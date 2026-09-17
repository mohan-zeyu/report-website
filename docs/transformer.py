import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention(nn.Module):
    r"""
    Dimension of input x in [N, n_seq, d_em]
    """
    def __init__(self, 
                 d_k: int = 32,
                 d_em: int = 16,
                 num_heads: int = 4,
                 max_len: int = 128,
                 batch: int = 4
                 ) -> None:
        super().__init__()
        assert d_k % num_heads == 0
        self.d_k = d_k
        self.d_em = d_em
        self.num_heads = num_heads
        self.batch = batch
        self.W_q = nn.Linear(d_em, d_k)
        self.W_k = nn.Linear(d_em, d_k)
        self.W_v = nn.Linear(d_em, d_k)
        self.W_o = nn.Linear(d_k, d_em)
        print(f"[Attention]: The d_k is {self.d_k}")
        print(f"[Attention]: The d_em is {self.d_em}")
        self.kv_cache = KVCache(d_k, num_heads, max_len, batch)

    def _convert(self, w: torch.Tensor, num_heads: int) -> torch.Tensor:
        N, n_seq, _ = w.shape
        return w.reshape(N, n_seq, num_heads, -1).transpose(1, 2)

    def forward(self, 
                x: torch.Tensor, 
                mask: torch.Tensor = torch.tensor(0),
                ) -> torch.Tensor:

        if x.shape[0] != self.batch:
            raise ValueError
        # Note that the KVCache should be model unaware
        # So we just simply compute the new one and then insert it in.
        Q = self._convert(self.W_q(x), self.num_heads)
        new_K = self._convert(self.W_k(x), self.num_heads) \
                    .squeeze(dim=1)
        new_V = self._convert(self.W_v(x), self.num_heads) \
                    .squeeze(dim=1)

        self.kv_cache.update(new_K, new_V)
        K, V = self.kv_cache.get()

        ratio = (F.softmax(Q @ torch.transpose(K, -1, -2) / math.sqrt(self.d_k / self.num_heads) + mask, dim=-1)) @ V
        N, n_seq, _ = x.shape
        ratio = ratio.transpose(1, 2).reshape(N, n_seq, self.d_k)
        y = self.W_o(ratio)
        return y

class KVCache():
    def __init__(self,
                 d_k: int,
                 num_heads: int,
                 max_len: int,
                 batch: int = 1
                 ) -> None:
        # it can't mismatch
        self.batch = batch
        self.max_len = max_len
    # we do not need to assert because it has been done in attention
        self.d = d_k // num_heads
        self.num_heads = num_heads
        self.k = torch.zeros((batch, max_len, num_heads, self.d))
        self.v = torch.zeros((batch, max_len, num_heads, self.d))
        self.counter = 0

    def get(self) -> tuple[torch.Tensor, torch.Tensor]:
        return self.k[:, :self.counter, :, :], \
               self.v[:, :self.counter, :, :]

    def update(self, new_k, new_v) -> bool:
        if self.counter == self.max_len - 1:
            return False

        # Now it seems that we could afford multiple tokens for decoding
        len = new_k.shape[1]
        self.k[:, self.counter: self.counter + len, :, :] = new_k
        self.v[:, self.counter: self.counter + len, :, :] = new_v

        self.counter += len
        return True


class Decoder(nn.Module):
    def __init__(self,
                 d_k: int = 32,
                 d_em: int = 16,
                 num_heads: int = 4,
                 max_len: int = 128,
                 batch: int = 4
                 ) -> None:
        super().__init__()
        self.d_hid = 4 * d_em
        self.attention = Attention(d_k, d_em, num_heads, max_len, batch)
        self.ffn = nn.Sequential(
            nn.Linear(d_em, self.d_hid),
            nn.GELU(),
            nn.Linear(self.d_hid, d_em)
        )
        self.ln_att = nn.LayerNorm(d_em)
        self.ln_ffn = nn.LayerNorm(d_em)

    def _gen_mask(self, 
                  sz: int,
                  device: torch.device,
                  dtype: torch.dtype
                  ) -> torch.Tensor:
        return torch.triu(torch.full((sz, sz), float('-inf'), dtype=dtype, device=device), diagonal=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mask = self._gen_mask(x.shape[-2], x.device, x.dtype)
        x = self.ln_att(x + self.attention(x, mask=mask))
        x = self.ln_ffn(x + self.ffn(x))
        return x
