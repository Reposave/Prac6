## Client Code.

To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device.
Once you are set up with balena, you will need to clone this repo locally:
```
$ git clone git@github.com:Reposave/Prac6.git
```
Then add your balena application's remote:
```
$ git remote add balena username@git.balena-cloud.com:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push balena master
```
It should take a few minutes for the code to push.

The Client will send a sample of data every 10s. Messages start with a code first before being sent.

Message symbol:
c - check
o - sendon
x - sendoff
s - sensors

After the symbol, some messages contain the number of bytes and then the message.


