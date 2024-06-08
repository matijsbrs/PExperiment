import ollama
import sys

def describe(image_path):
	print("Describing image: " + image_path)
	res = ollama.chat(
		model="llava",
		messages=[
			{
				'role': 'user',
				'content': 'Describe this image:',
				'images': ['./Programming\ bear2.jpg']
			}
		]
	)
	
	print(res['message']['content'])


def describe_pro(image_path):
    print("Describing image: " + image_path)
	
    res = ollama.chat(
        model="llava-llama3",
        messages=[
            {
                'role': 'system',
                'content': """
					You are a photo analysis model that describes the content of images in detail.
					Describe te following:
					* general scene.
					* objects up to 5 objects.
					* Create a list of up to 10 tags.
					"""
            },
            {
                'role': 'user',
                'content': 'Describe this image and provide tags:',
                'images': ['./Programming bear2.jpg']
            }
        ]
    )
    return res

if __name__ == "__main__":
	image_path = "./.jpg"  # Replace with the actual path to the image file
	if len(sys.argv) > 1:
		image_path = sys.argv[1]
	else:
		image_path = "./Programming\ bear2.jpg"  # Replace with the default image path

	info = describe_pro(image_path)
	print(info['message']['content'])

