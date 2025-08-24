import express from "express";
import cors from "cors";
const app = express();
const PORT = 4100;
import puppeteer from "puppeteer";

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  return res.sendStatus(200);
});

app.post("/image", async (req, res) => {
  const code = req.body.code;
  console.log(req.body);
  console.log("generating image.....");

  try {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.setContent(
      `<div style="width:1200px;min-height:675;background:black;display:flex;justify-content:center;align-items:center">
          <pre style="max-width:85%;margin-top:50px;margin-bottom:50px;border-radius:10px;font-family: monospace;font-size:22px;padding:30px;background:white;color:black;font-weight:medium;word-wrap:break-word;white-space:pre-wrap;">${code}</pre>
      </div>`
    );
    const element = await page.$("div");

    const bufferImage = await element.screenshot();
    await browser.close();
    console.log("Image generated.");

    res.setHeader("Content-Type", "image/png");
    return res.status(200).send(bufferImage);
  } catch (error) {
    console.log(error);
    return res.sendStatus(400);
  }
});

app.listen(PORT, () => {
  console.log("Running sever at https://localhost:" + PORT);
});
