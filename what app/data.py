import os

# รับ path ปัจจุบันและชื่อไฟล์
dirname, filename = os.path.split(os.path.abspath(__file__))
print(dirname, filename)

# สร้างข้อมูลเทส
data = [
    {
        'name': 'Ellie Clark',
        'dp': 'i1.jpg',
        'chats': {
            'there': ["Hi!", "How are you", "I am good", "will you go there tomorrow"],
            'here': ["Hello", "I am fine", "you ?"]
        }
    },
    {
        'name': 'Lisa Webb',
        'dp': 'i2.jpg',
        'chats': {
            'there': ["Hi, how’re you?", "Good. How’s your work going on?", "Why? What happened?", "Then?", "Got it. So have you been applying elsewhere?", "Sending resumes cold doesn’t work well. Off hand, I don’t recall a contact in your industry, but lemme try through people I know. I’ll let you know."],
            'here': ["I’m fine. What about you?", "Not great.", "I can’t cope up with my manager. He was fine to begin with, but not anymore. But that’s not the only reason.", "Also, the commute time to the office is just too much at the moment, and I don’t foresee a shift to a closer location in this organization. Too much time on the road is taking a toll on me.", "I am, but the route of sending resumes and cover letters has so far not yielded much. It seems as if they’re disappearing into a black hole, with little to no response coming. Do you know persons in the industry who can help me land interviews?", "Thanks."]
        }
    },
    # เพิ่มข้อมูลอื่นๆ ตามต้องการ
]

print(data[0]['name'], data[0]['dp'], data[0]['chats']['there'], data[0]['chats']['here'])
