# emotion demo für PIT Hackathon
# Autor: Georg Begerow gbegerow@netatwork.de
# Aufruf der Cognitive Services Emotion API via Phython
# Geschrieben für Phyton > 3.6, für 2.7 müssen einige Dinge wie f-Strings umgeschrieben werden

import http.client, urllib.request, urllib.parse, urllib.error, base64, os, json, sys

def main(argv):
    imageUrl = "https://azurecomcdn.azureedge.net/cvt-70f5720cd71339ab321f5174fee8215e3f5363ee1e7162647cfdb4e0c0914ea2/images/shared/cognitive-services-demos/recognize-emotion/emotion-3-thumbnail.jpg"

    # analysiere image via url 
    analysisJson = recognize(imageUrl)
    #print(analysisJson)
    
    # erzeuge python object aus json
    analysis = json.loads(analysisJson)
    print(f"Gefunden: { len(analysis) } Gesicht/er")

    # finde die stärkste Emotion des ersten gefundenen Gesichtes
    emotion = findEmotion(analysis[0])
    #print(emotion)
    
    # zeige als Emoji an
    emoji = EmotionToEmoji(emotion)

    # windows console kann leider mit den meisten emoji nicht umgehen 😠
    print(f"{emotion}: {emoji}")

    # in eine datei schreiben und im Browser starten, da wird das richtig angezeigt
    with open('emotion.html','w',encoding='utf-8-sig') as f:
        f.write(f"{emotion}: {emoji}")
    os.startfile('emotion.html')


def recognize(imageUrl):
    # für Testzwecke, Ergebnis des standard images
    return '[{"faceRectangle":{"height":36,"left":0,"top":59,"width":36},"scores":{"anger":1.20879849E-06,"contempt":9.064575E-07,"disgust":7.811325E-06,"fear":3.73563E-11,"happiness":0.999936461,"neutral":5.35512263E-05,"sadness":7.13684667E-10,"surprise":4.32085123E-08}}]'

    # Unser subscription key muss sich in der Environmentvariable CS_EMOTION_KEY befinden. (Secrets gehören nicht in den Code)
    # print(os.environ["CS_EMOTION_KEY"])
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': os.environ["CS_EMOTION_KEY"]# '{subscription key}',
    }

    # zusätzliche url parameter, im Moment keine
    params = urllib.parse.urlencode({
    })

    try:
       #
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, '{"url":"' % imageUrl % '"}', headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()

        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Suche die Emotion mit der höchsten Bewertung
def findEmotion(analysis):
    highestEmotion = None
    highestEmotionValue = -1

    for emotion, value in analysis["scores"].items():
        if value > highestEmotionValue:
            highestEmotion=emotion
            highestEmotionValue = value

    return highestEmotion

# 
def EmotionToEmoji(emotion):
    # Achtung, je nach eingestelltem Font im Editor sind hier die Emojis selbst zu sehen oder nur platzhalter zeichen
    emojis = {
        "anger":"😠", # https://emojipedia.org/angry-face/
        "contempt":"🙄", # https://emojipedia.org/face-with-rolling-eyes/
        "disgust":"🤢", # https://emojipedia.org/nauseated-face/
        "fear":"😱", # https://emojipedia.org/face-screaming-in-fear/
        "happiness":"😃", # https://emojipedia.org/smiling-face-with-open-mouth/
        "neutral":"😐", # https://emojipedia.org/neutral-face/
        "sadness":"😢", # https://emojipedia.org/crying-face/
        "surprise":"😲" # https://emojipedia.org/astonished-face/
    }
    #print(emojis)

    return emojis[emotion]


if __name__ == "__main__":
    main(sys.argv)