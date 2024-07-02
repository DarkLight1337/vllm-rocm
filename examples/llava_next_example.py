from io import BytesIO

import requests
from PIL import Image

from vllm import LLM, SamplingParams

# The assets are located at `s3://air-example-data-2/vllm_opensource_llava/`.
# You can use `.buildkite/download-images.sh` to download them


def run_llava_next():
    llm = LLM(
        model="llava-hf/llava-v1.6-mistral-7b-hf",
        image_token_id=32000,
        image_input_shape="1,3,336,336",
        image_feature_size=1176,  # The value does not matter
    )

    prompt = "[INST] <image>\nWhat is shown in this image? [/INST]"
    url = "https://h2o-release.s3.amazonaws.com/h2ogpt/bigben.jpg"
    image = Image.open(BytesIO(requests.get(url).content))
    sampling_params = SamplingParams(temperature=0.8,
                                     top_p=0.95,
                                     max_tokens=100)

    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {
                "image": image
            }
        },
        sampling_params=sampling_params)

    generated_text = ""
    for o in outputs:
        generated_text += o.outputs[0].text

    print(f"LLM output:{generated_text}")


if __name__ == "__main__":
    run_llava_next()
