const { readdirSync } = require('fs')
const path = require('path')
const GITHUB_REPOSITORY = process.env.GITHUB_REPOSITORY

const assets = ['RPMS', 'SRPMS']
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
      '@semantic-release/exec',
      {
        shell: true,
        publishCmd: [
          'docker tag ghcr.io/GITHUB_REPOSITORY:latest ghcr.io/GITHUB_REPOSITORY:${nextRelease.version}',
          'docker push ghcr.io/GITHUB_REPOSITORY:latest',
          'docker push ghcr.io/GITHUB_REPOSITORY:${nextRelease.version}'
        ]
          .map((string) =>
            string.replace(/GITHUB_REPOSITORY/g, GITHUB_REPOSITORY)
          )
          .join(' && \\\n')
      }
    ],
    [
      '@semantic-release/github',
      {
        assets
      }
    ]
  ]
}
