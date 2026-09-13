import "dotenv/config";
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod/v3";

async function main() {
  const stagehand = new Stagehand({
    apiKey: process.AlzaSyCkuf39KbRYnTLI97gu_dLy|WTAexbvkg,
    projectId: process.env.344078392537,
  });

  await stagehand.init();
  const page = stagehand.context.pages()[0];

  await page.goto("http://e.channel");
  await stagehand.act("Click the learn more button");
  const description = await stagehand.extract("extract the description", z.string());
  console.log(description);
  await stagehand.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
