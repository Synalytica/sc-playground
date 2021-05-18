# Smart Contract Playground

## Running

1. Install [Docker](https://www.docker.com/), if not already installed.
2. Run `sudo docker build -t sc_play .` from project root
3. Run `sudo docker run -i -d --name sc_play -v $PWD:/app sc_play`

## Testing Smart Contracts

- Testing Single Smart Contract

  1. Run `sudo docker exec sc_play ./test.sh {path}`, where `{path}` is the path of smart contract from project root.

- Testing all Smart Contracts at once

  1. Make sure all the smart contracts are in `/contracts/`
  2. Run `sudo docker exec sc_play ./test.sh`
