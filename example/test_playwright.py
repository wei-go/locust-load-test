# Demonstrates the two ways to run Playwright (prerecorded script or "manual")

# Notes:
# Dont forget to first install the browsers by running: playwright install
# Browsers are heavy. Dont expect to be able to do as much load as usual with Locust. Optimize your tests by blocking requests for unnecessary resources.
# Dont run too many users per worker instance (or you'll get the dreaded "CPU usage over 90%" warning). Instead, scale using more Locust workers. 4-5 users/browsers per workers seems ok. If you are using locust-swarm, increase the --processes-per-loadgen parameter.
# Some things, such as adding request callbacks (Page.route()), will cause intense communication with the browser will overload Python/Playwright so be careful.
# It is easy to accidentally make Playwright tests stall for a long time, for example if your page does finish loading completely (triggering the "load" event). Experiment with alternative wait strategies (e.g. wait_until="domcontentloaded" or self.page.wait_for_selector(...))


from locust import run_single_user, task
from locust_plugins.users.playwright import PageWithRetry, PlaywrightUser, PlaywrightScriptUser, pw, event
import time


# class ScriptBased(PlaywrightScriptUser):
#     # run a script that you recorded in playwright, exported as Python Async
#     # script = "playwright-recording.py"
#     pass


class Manual(PlaywrightUser):
    host = "https://docs.locust.io/en/latest"
    multiplier = 10  # run ten concurrent playwright sessions/browsers for each Locust user. This helps improve load generation efficiency.

    @task
    @pw
    async def locust_goto_website(self, page: PageWithRetry):
        try:
            async with event(self, "Load up Locust Document"):  # log this as an event
                await page.goto("/")  # load a page

            async with event(self, "Go to Locust.io"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    action = '#locust-documentation > div.sidebar > ul > li:nth-child(1) > p > a'
                    await page.click(action) 
                    # sometimes even Playwright has issues with stability (especially under high load)
                    # await page.click_retry(action, retries=1)
                    await page.wait_for_timeout(1000)
                    await page.screenshot(path=f"locust_goto_website_{time.time()}.png")
        except:
            pass

    @task
    @pw
    async def locust_goto_git(self, page: PageWithRetry):
        try:
            async with event(self, "Load up Locust Document"):  # log this as an event
                await page.goto("/")  # load a page

            async with event(self, "Go to Git"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    action = 'body > div.wy-grid-for-nav > section > div > div > div:nth-child(1) > ul > li.wy-breadcrumbs-aside > a'
                    await page.click(action)
                    await page.wait_for_timeout(1000)
                    await page.screenshot(path=f"locust_goto_git_{time.time()}.png")
        except:
            pass


# class OneMegabitUserThatMeasuresLCP(PlaywrightUser):
#     host = "https://docs.locust.io/en/latest"

#     @task
#     @pw
#     async def google(self, page: PageWithRetry):
#         # start CDP (chrome dev tools)
#         self.client = await self.browser_context.new_cdp_session(self.page)
#         await self.client.send("Network.enable")
#         await self.client.send(
#             "Network.emulateNetworkConditions",
#             {
#                 "offline": False,
#                 "downloadThroughput": (1 * 1024 * 1024) / 8,
#                 "uploadThroughput": (1 * 1024 * 1024) / 8,
#                 "latency": 50,
#             },
#         )
#         self.start_time = time.time()
#         async with event(self, "Load up Locust Document"):  # log this as an event
#             await page.goto("/")  # load a page

#         await page.wait_for_timeout(1000)  # just in case there is an even larger contentful paint later on
#         lcp = await page.evaluate(
#             """
#         new Promise((resolve) => {
#             new PerformanceObserver((l) => {
#                 const entries = l.getEntries()
#                 // the last entry is the largest contentful paint
#                 const largestPaintEntry = entries.at(-1)
#                 resolve(largestPaintEntry.startTime)
#             }).observe({
#                 type: 'largest-contentful-paint',
#                 buffered: true
#             })
#         })
#         """
#         )
#         self.environment.events.request.fire(
#             request_type="LCP",
#             name="LCP",
#             start_time=self.start_time,
#             response_time=lcp,
#             response_length=0,
#             context={**self.context()},
#             url="casino_LCP",
#             exception=None,
#         )


if __name__ == "__main__":
    run_single_user(Manual)