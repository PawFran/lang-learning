if __name__ == '__main__':
    from openai import OpenAI
    import sys

    client = OpenAI()

    if len(sys.argv) == 1:
        raise Exception('You must give at least one word')

    prompt = ' '.join(sys.argv[1:])

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(completion.choices[0].message.content)
