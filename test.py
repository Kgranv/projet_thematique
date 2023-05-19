import asyncio
import time

async def runPompe(index,dutyCycle):
    print("Demarage pompe ",index)
    await asyncio.sleep(1*2)
    print("Fin test pompe ",index)

async def main():
    dc = [50.0,54.2,58.3,62.5,66.7,70.8,75.0,79.2,83.3,87.5,91.7,95.8,100]
    tension = [6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0]
    test = []
    for x in range(0,len(dc)):
        print("Test avec une tension de ",tension[x]," V :")
        input('Presser entrer pour commencer ')
        for i in range(0,3):
            test.append(asyncio.create_task(runPompe(motor[i],dc[x])))
        await test[0]
        await test[1]
        await test[2]
        test = []
        
motor = [1,2,3]
asyncio.run(main())
