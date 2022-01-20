const { readdirSync } = require('fs')
const path = require('path')

const assets = ['RPMS'/* ,'SRPMS' */]
  .flatMap((folder) => readdirSync(path.join(__dirname, folder))
    .map((name) => path.join(__dirname, folder, name))
  )
  .filter((value) => path.extname(value) === '.rpm')
  .map((path) => ({ path }))

module.exports = {
  branches: ['trunk'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    [
      '@semantic-release/github',
      {
        assets
      }
    ]
  ]
}
