# Personal Assistant for Communication Analysis and Improvement

This code repository accompanies the hackster submission "Personal Assistant for Communication Analysis & Improvement" by Selina Meyer and Samy Ateia to the *AMD Pervasive AI Developer Contest*

Our project consisted of three phases: 
1. Generation of simulated chats between persons with different types of relationships and corresponding advice using state-of-the-art LLMs. The code for this is found in [chat-advice-generation](https://github.com/SelinaMeyer/personal-assistant-for-communication-analysis-and-improvement/chat-advice-generation)
2. Creation and evaluation of an advice-rater model to evaluate the quality of advice given by LLMs, using crowdworker judgements as ground truth. The code for the survey to solicit ratings from crowdworkers and creating the rater model can be found in [advice-judgement-survey](https://github.com/SelinaMeyer/personal-assistant-for-communication-analysis-and-improvement/advice-judgement-survey)
3. Few-shot learning a small LLMs as basis for a secure and locally running personal assistant to provide advice on social communication. The code to run the assistant can be found in [assistant](https://github.com/SelinaMeyer/personal-assistant-for-communication-analysis-and-improvement/assistant)