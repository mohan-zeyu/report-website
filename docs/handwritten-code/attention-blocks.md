# Transformer and KV Cache Basics
## Build Attention, then Decoder class

Since it has been so long since i read the paper "Attention is All You Need", i'm trying to write the code from scratch based on the incomplete impression, attempting to reconstruct the whole and detailed map by trial and error.  
The basic idea of above words is just to make all dimensions of layers' input and output match, and finally, a forward computation can be done. To make it work, it definitely cost me much time.  
Since i already completed the writing of `Decoder` before i write these words, so i will directly present the code here.

```python linenums="1"
class Attention(nn.Module):
    r"""
    Dimension of input x in [N, n_seq, d_em]
    """
    def __init__(self, 
                 d_k: int = 32,
                 d_em: int = 16,
                 num_heads: int = 4
                 ) -> None:
        super().__init__()
        assert d_k % num_heads == 0
        self.d_k = d_k
        self.d_em = d_em
        self.num_heads = num_heads
        self.W_q = nn.Linear(d_em, d_k)
        self.W_k = nn.Linear(d_em, d_k)
        self.W_v = nn.Linear(d_em, d_k)
        self.W_o = nn.Linear(d_k, d_em)
        print(f"[Attention]: The d_k is {self.d_k}")
        print(f"[Attention]: The d_em is {self.d_em}")

    def _convert(self, w: torch.Tensor, num_heads: int) -> torch.Tensor:
        N, n_seq, _ = w.shape
        return w.reshape(N, n_seq, num_heads, -1).transpose(1, 2)

    def forward(self, 
                x: torch.Tensor, 
                mask: torch.Tensor = torch.tensor(0),
                ) -> torch.Tensor:
        Q = self._convert(self.W_q(x), self.num_heads)
        K = self._convert(self.W_k(x), self.num_heads)
        V = self._convert(self.W_v(x), self.num_heads)

        ratio = (F.softmax(Q @ torch.transpose(K, -1, -2) / math.sqrt(self.d_k / self.num_heads) + mask, dim=-1)) @ V
        N, n_seq, _ = x.shape
        ratio = ratio.transpose(1, 2).reshape(N, n_seq, self.d_k)
        y = self.W_o(ratio)
        return y

class Decoder(nn.Module):
    def __init__(self,
                 d_k: int = 32,
                 d_em: int = 16,
                 num_heads: int = 4,
                 ) -> None:
        super().__init__()
        self.d_hid = 4 * d_em
        self.attention = Attention(d_k, d_em, num_heads)
        self.ffn = nn.Sequential(
            nn.Linear(d_em, self.d_hid),
            nn.GELU(),
            nn.Linear(self.d_hid, d_em)
        )
        self.ln_att = nn.LayerNorm(d_em)
        self.ln_ffn = nn.LayerNorm(d_em)

    def _gen_mask(self, sz: int) -> torch.Tensor:
        return torch.triu(torch.full((sz, sz), float('-inf')), diagonal=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mask = self._gen_mask(x.shape[-2])
        x = self.ln_att(x + self.attention(x, mask=mask))
        x = self.ln_ffn(x + self.ffn(x))
        return x
```

### issues
As you can see, it looks very good. And if you create a `main.py` to give it an input and it will do perfectly as we expected.  
But for serious work, there are still things to do:

1. where the model lives.

    Since model typically runs on GPU, here's another perspective we should consider in coding.  
    Look at the `_gen_mask` method:

    ```python linenums="1"
    def _gen_mask(self, sz: int) -> torch.Tensor:
        return torch.triu(torch.full((sz, sz), float('-inf')), diagonal=1)
    ```

    Here, i created a brand new tensor, which won't follow the model

2. data types. Let's just do `model.to(device, torch.bfloat16)` when moved to GPU

In this case now, it looks like we have done lot's of things, core components got.
## KV Cache  
I haven't implemented it before by hand.

Let's solve the problem by asking questions:

### Conceptually

#### What does the KV cache store and how does it store data?

Write the attention formula manually then we will find the formula like this for every query $q_n$:

$$
scores = \left[ score(q_n^Tk_1), \dots , score(q_n^Tk_n)\right] = Softmax(\left[ q_n^Tk_1, \dots, q_n^Tk_n\right])
$$

$$
attention_{token_n} = \sum_{i=1}^{n}score(q_n^Tk_i)v_i^T
$$

And we will find that all $k_i$ before n can be reused.
Honestly, I kept wondering why we don't just store the product of K and V days ago and now I find that I missed softmax function in the middle.
So, actually, the KV cache is two separate buffers for storing K and V respectively.

#### What are decoding and prefill phases?

For a decoder-only model, you can't let it start to output from empty tokens. So initially some tokens will be sent first, and based on that, model will start talking. Also, it's the stage for storing KV cache.
So the process that first N tokens come up is called prefill, at which the KV cache is computed. Because it's the $O(N^2)$ process, it's computation-bound, requiring lots of parallel computings like GEMM.

Then after k and v of previous tokens have been got. We will just send maybe one token a time and then use the previous cache, which requires much less computations but one can imagine that there will be so much data transferring between HBM and cache to and from.
So it's memory bandwidth bound.

Note that for decoder-only model, we only need the last token's result to evaluate next token.

### Engineering
1.  KV_cache should be moved to GPU as well.
	Internally, we set k and v tensors to be buffers of pytorch, data of which will then follow with the model
	```python
	self.register_buffer('k',
						torch.empty((batch, num_heads, self.max_len, self.d)),
						persistent=False
						)
	self.register_buffer('v',
					torch.empty_like(self.k),
					persistent=False
					)
	```
	Note that here we pre-allocate some memory for storing kv cache.

2. The weights are kept in memory but KV cache will change constantly.

	We setup methods for clearing content in kv cache along the composition, from Decoder to Attention and to kv_cache.
	
	The way to clear kv_cache is simply reset the counter:
	```python
	def clear(self) -> None:
        self.counter = 0
	```

3. training shouldn't use kv cache. So how to design the class? And gradients are also not required.

	Add additional property to judge whether to use KV cache for generation.
	```python
    @property
    def use_cache(self) -> bool:
        return not self.training
	```
	Then before KV calculation, ask it first.
	
4. How to separate prefill and decode phases in code? Mask Design
	Actually, we don't need to separate them, just treating them the same way. And remember to add KV cache by the input length, which is enough.
	
	For the mask, it's a point worth minding because it will no longer be previous square shape.
	
	For multi-token decoding phase, you need to prevent a very small triangular at the right top corner of the score matrix.
	```python
	q_len, k_len = Q.size(-2), K.size(-2)
	query_positions = torch.arange(k_len - q_len, k_len, device=Q.device)
	key_positions = torch.arange(k_len, device=Q.device)
	future = query_positions[:, None] < key_positions[None, :]
	```

5. How do we make sure that the `batch` is always matched.
	Note that there's a dimension of data, very strange and mysterious that we haven't care about it.
	
	For a deployed model for inference, I think the `batch` size has been set up initially. And later maybe backends will combine different user requests together into?
	But will it actually accelerate?
	
	Yes, definitely, because if the batch is not filled, then many GPU computing units will just be idle, only memory working hard. So gathering batches helps a lot for throughput.

This is the final code:

<div class="code-scroll-window">
  <div class="code-scroll-window__title" id="transformer-code-title">transformer.py</div>
  <div class="code-scroll-window__body" markdown="1" role="region" aria-labelledby="transformer-code-title" tabindex="0">

```python linenums="1"
--8<-- "docs/transformer.py"
```

  </div>
</div>



Another problem is from "GLM 5.3 Flash", it told me i haven't implemented `positional embedding`, so the "past" K/V are identical because they are simply computed by $W_k(x)$ and $W_v(x)$.


## **AI claim**  
For learning purpose because i think concepts here are important as foundation work, no code is generated by AI, so here may be some design flaws or bugs.
