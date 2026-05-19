all: dist/index.js

clean:
	rm -rf dist node_modules

node_modules/.package-lock.json: package.json package-lock.json
	npm install

dist/index.js: src/index.js rollup.config.js node_modules/.package-lock.json
	./node_modules/.bin/rollup --config rollup.config.js
