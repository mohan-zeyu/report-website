AI slop, especially for those text outputs from AI are usually the barrier for learners, especially for those whose first language is not English. 

No examples here but I indeed have seen many explanatory words from LLMs like Claude or ChatGPT. Especially for models from Anthropic but not limited to, they always use strange words to express some simple cases or meanings, for example, in a project about PCB boards temperature maps that I was just done, there will areas with low emissivity, as well as that of with high. But Claude then described the area with low emissivity as "footprint", which makes a lot trouble for me at first and it took me quite a long time to accept this concept.
Also, the likely cases happened many times before, and I tried many times to put claude's output to gpt for better clearness.

But now, Andrej Karpathy's latest post shed a light on the problem, which is amazing.

The link's here:
[https://x.com/karpathy/status/2105819303471976479](https://x.com/karpathy/status/2105819303471976479)

1. **Replace the English dictionary to a limited roughly 900 words.**

	Those words are from a set called ASD-STE100, written by people whose readers would die if a sentence could be read two ways. So it might be the strongest anti-slop method in the world.
	
	And I think the clearness will definitely helps a lot. People may be not struggle with strange definitions or expressions.

	But problems currently when I haven't tried it:
	
	1. How can it handle cases that out of current vocabulary? Things always change and maybe it won't be powerful enough in current general cases.
		So target to this, maybe we could try to build a field-only vocabulary, which will also be equipped with properties like ambiguity-free.
		
	2. .. to be continued
	
2. Using **visualizations** like images and later even for HTML page which can create animes or step "slides" for showing detailed processes, which, I think, is intuitive that every one can know the power. 

	I have been trying it till now. In most cases, I still have to pair with below description words so that I may manage to understand what it wants to tell me because not every concept can be understood easily at the first sight of its visualization.
	
3. **Creating a 3b1b style video**, err... , that's an amazing idea to let a model create a video for illustration. I haven't even think it before because in my long intuition, generating videos won't be cost-easy task. But with the continuous extending of model capability, things have changed.

	I'm now exploring this one.

	Oh MTF, we can program for videos, which is the "starting point" from GPT.
	[Manim](https://docs.manim.community/en/stable/tutorials/quickstart.html) Give it a look. It's so amazing.

	Oh! I can't say a word now. 
	Look at the video below after just one turn from gpt 6.1 sol (high) explaining the paper "EXPLORATION BY RANDOM NETWORK DISTILLATION"


<video controls width="100%">
  <source src="/assets/rnd-explainer.mp4" type="video/mp4">
</video>

I think, the quality is unbelievably great. Thanks Andrej!