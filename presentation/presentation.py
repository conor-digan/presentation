
import openai
import ast

SYSTEM_MESSAGE = '''You are PresentationGPT, a large language model trained by OpenAI. 
Your role is to help people craft engaging presentations according to their desires.'''

SCRIPT_TEMPLATE = '''
    I'm a giving a presentation on {topic}. I need to create a presentation of length {length} on this. 
    The audience is {audience} and my goal is to {goal}.
    
    The important points I would like to cover are: {important_points}
    
    Prepare the script for this presentation. Please output this script as a list of slides in the following json format:
    [
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    .....
    ]

'''

UPDATE_TEMPLATE = '''
Please update the script according to the following instructions:
{user_feedback}

Please output the updated script as a list of slides in the following json format:
    [
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    {{
        slide_number: '..'
        slide_title: '..'
        script: '..'
    }},
    .....
    ]
'''

SLIDE_TEMPLATE = '''
    Slide Number: {slide_number}\n
    Slide Title: {slide_title}\n
    Content:
    {slide_content}\n
'''

class Slide():
    pass

class Presentation():

    def __init__(self):
        pass

    def get_whole_script(self):

        script = ''
        for slide in self.slides:
            slide_script = SLIDE_TEMPLATE.format(
                slide_number = slide.slide_number,
                slide_title = slide.slide_title,
                slide_content = slide.script
                )

            script = '''{existing_script}
            
            {new_slides_script}'''.format(
                existing_script=script, 
                new_slides_script=slide_script
                )

        return script

    def generate_script(self, topic, audience, length, goal, important_points):

        # Initialise the basic presentation config
        self.topic = topic
        self.audience = audience
        self.length = length
        self.goal = goal
        self.important_points = important_points

        # Generate the prompt to be used to generate the presentations script
        script_prompt = SCRIPT_TEMPLATE.format(
            topic=topic, 
            audience=audience, 
            length=length, 
            goal=goal,
            important_points=important_points
        )

        # Combine the prompt with the system message in the foramt required by GPT
        messages = [
            {'role': 'system', 'content': SYSTEM_MESSAGE},
            {'role': 'user', 'content': script_prompt}
            ]
            
        # Generate the script using GPT
        script = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
                temperature = 0.0,
            )["choices"][0]["message"]["content"]

        messages.append({'role': 'assistant', 'content': script})

        # Set the messages & script variables
        self.messages = messages
        print(script)
        self.slides = self._extract_slides_from_raw_script(script)


    def update_script(self, user_feedback):

        update_prompt = UPDATE_TEMPLATE.format(user_feedback=user_feedback)

        # Add the new prompt to the messages
        self.messages.append({'role': 'user', 'content': update_prompt})

        # Generate the new script using GPT
        new_script = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
                temperature = 0.0,
            )["choices"][0]["message"]["content"]

  
        self.messages.append({'role': 'assistant', 'content': new_script})
        self.slides = self._extract_slides_from_raw_script(new_script)


    def _extract_slides_from_raw_script(self, raw_script):

        slides = []

        cleaned_script = '[' \
            + ''.join(
                ''.join(raw_script.split('[')[1:])
                .split(']')[:-1]
            ) \
            + ']'
        
        dict_script = ast.literal_eval(cleaned_script)

        for values in dict_script:
            s = Slide()
            s.slide_number = values['slide_number']
            s.slide_title = values['slide_title']
            s.script = values['script']
            slides.append(s)

        return slides