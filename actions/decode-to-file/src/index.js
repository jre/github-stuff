import * as core from "@actions/core";
import { Buffer } from "node:buffer";
import * as fs from "node:fs/promises";

try {
    const data = Buffer.from(core.getInput("data", { required: true }),
			     core.getInput("encoding", { required: true }));
    const filename = core.getInput("filename", { required: true });
    const mode = parseInt(core.getInput("mode", { required: true }), 8);

    try {
	await fs.unlink(filename);
    } catch (err) {
	if (err.code !== "ENOENT")
	    throw err;
    }

    let fd;
    try {
	fd = await fs.open(filename, "wx", mode);
	await fs.writeFile(fd, data);
    } finally {
	await fd?.close();
    }
} catch (err) {
    core.setFailed(err.message);
}
