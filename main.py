from CCGPT.CCGPT import CCGPT

ccgpt = CCGPT()
ccgpt.train()
ccgpt.start()

try:
    ccgpt.chat()
except:
    pass

ccgpt.quit()