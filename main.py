from CCGPT.CCGPT import CCGPT
import sys
sys.stderr.close()


ccgpt = CCGPT()
ccgpt.train()
ccgpt.start()

try:
    ccgpt.chat()
except Exception as e:
    # pass
    print(e)

ccgpt.quit()