import * as core from "@actions/core";
import * as fs from "node:fs/promises";
import * as nj from "nunjucks";

try {
    const infile = core.getInput("template-file", { required: true });
    const outfile = core.getInput("output-file", { required: true });
    const url = core.getInput("redirect-url", { required: true });

    fs.writeFile(outfile, nj.render(infile, { url: url }));
} catch (err) {
    core.setFailed(err.message);
}
