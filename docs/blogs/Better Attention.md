# Better Attention
## Introduction

Attention mechanism has been widely used in modern neural networks, across multiple areas like large language model, image generation, audio recognition. However, it has become a bottleneck gradually along with the scaling of today's models, both in computation and memory. This essay intends to summarize what people did in last few years aiming to reduce the cost both in computation and memory of the Attention, especially at K and V representation, storage, retrieval and update.

## Time and Space costs of KV Cache

Let's assume there are $l$ layers of attention, each with $h$ heads. Every head contains $d$ dimensions for $k$ and $v$ each. The sequence length is $n$.

During prefill stage, we generate the KV cache by $O(n^2hdl)$ computation.