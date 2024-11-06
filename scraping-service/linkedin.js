import { launch, Browser, Page } from 'puppeteer';

export class LinkedInScraper {
  /**
   * @type {Browser | undefined}
   */
  #browser;

  constructor() {
  }

  async initialise() {
    this.#browser = await launch({headless: true});
  }

  /**
   * 
   * @param {string} userid 
   * @param {string} password 
   */
  async login(userid, password) {
    let page = await this.#browser.newPage()
    await page.goto("https://www.linkedin.com/login");
    await page.waitForNetworkIdle({idleTime: 500});
    await page.evaluate((username, password) => {
      /**
       * @type {HTMLInputElement}
       */
      let userid_input = document.getElementById("username");
      userid_input.value = username;
      /**
       * @type {HTMLInputElement}
       */
      let password_input = document.getElementById("password");
      password_input.value = password;
      /**
       * @type {HTMLButtonElement}
       */
      let submit_button = document.querySelector('button[type="submit"]');
      submit_button.click()
    }, userid, password);
    try{
      console.log("starting wait")
      await page.waitForNetworkIdle({idleTime: 500});
    } catch (err) {
      console.warn("Failed waiting for login networkidle. Hopefully it still works")
      console.error(err);
    }
    console.log("completed login")
    return page;
  }

  /**
   * 
   * @param {Page} page
   * @param {string} profileHandle 
   */
  async fetchProfileMetadata(page, profileHandle) {
    await page.goto(`https://www.linkedin.com/in/${profileHandle}/`)
    try {
      await page.waitForNetworkIdle({idleTime: 500});
    } catch(err) {
      console.warn("Failed waiting for network idle on target profile. Hopefully it still works");
      console.error(err);
    }
    return await page.evaluate(() => {
      return {
        name: document.querySelector("h1")?.textContent?.trim(),
        headline: document.querySelector("div[data-generated-suggestion-target]")?.textContent?.trim(),
        about: document.querySelectorAll("div[data-generated-suggestion-target]")[1]?.textContent?.trim()
      }
    });
  }

  /**
   * 
   * @param {Page} page 
   * @param {string} profileHandle 
   */
  async fetchLatest5Posts(page, profileHandle) {
    await page.goto(`https://www.linkedin.com/in/${profileHandle}/recent-activity/all/`);
    try {
      await page.waitForNetworkIdle({idleTime: 500});
    } catch(err) {
      console.warn("Failed waiting for network idle on target posts. Hopefully it still works");
      console.error(err);
    }
    return await page.evaluate(() => {
      let postContainers = document.querySelectorAll("div.scaffold-finite-scroll ul>li.profile-creator-shared-feed-update__container");
      let posts = []
      for (let postContainer of postContainers) {
        if (posts.length == 5) {
          break
        }
        postContainer.scrollIntoView()
        let timeAgo = postContainer.querySelectorAll("div>div>a")[3]?.querySelector("span>span")?.textContent.replace("•", "").trim();
        let content = postContainer.querySelector("div.feed-shared-update-v2__description-wrapper").textContent.trim();
        if (content.endsWith("\n...more")) {
          content = content.substring(0, content.length-8);
        }
        posts.push({timeAgo, content})
      }
      return posts
    });
  }

  async close() {
    return await this.#browser.close();
  }
}
