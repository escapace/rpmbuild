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
    process.env['RELEASE_CONTAINER'] === 'true' ? [
      '@semantic-release/exec',
      {
        shell: true,
        publishCmd: [
          [
            'docker buildx build',
            '--cache-from type=local,src=$HOME/.buildx',
            '--cache-to   type=local,dest=$HOME/.buildx,mode=max',
            '--platform linux/amd64,linux/arm64/v8',
            '--tag ghcr.io/GITHUB_REPOSITORY:latest',
            '--tag ghcr.io/GITHUB_REPOSITORY:${nextRelease.version}',
            '--push .'
          ].join(' ')
        ]
          .map((string) =>
            string.replace(/GITHUB_REPOSITORY/g, GITHUB_REPOSITORY)
          )
          .join(' && \\\n')
      }
    ] : undefined,
    process.env['RELEASE_ASSETS'] === 'true' ? [
      '@semantic-release/github',
      {
        assets
      }
    ] : undefined,
  ].filter((value) => value !== undefined)
}
