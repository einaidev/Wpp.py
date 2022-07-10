import asyncio


def CatchErros(driver):
    def decorator(f):
            try:
                f()
            except Exception as e:
                driver.close()
                driver.quit()
                print(e)
                exit()
    return decorator

def AsyncCatchErros(driver):
    loop = asyncio.get_event_loop()
    def decorator(f):
        async def w():
            try:
                await f()
            except Exception as e:
                driver.close()
                driver.quit()
                print(e)
                exit()
        loop.run_until_complete(w())
    return decorator

def async_error_resolve(f,driver):
    loop = asyncio.get_event_loop()
    async def w(): 
        try:
            await f()
        except Exception as e:
            driver.close()
            driver.quit()
            print(e)
            exit()
    loop.run_until_complete(w())

def error_resolve(f,driver):
    loop = asyncio.get_event_loop()
    def w(): 
        try:
            f()
        except Exception as e:
            driver.close()
            driver.quit()
            print(e)
            exit()
    w()