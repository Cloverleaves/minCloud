minCloud
========

A ready-to-serve cloud server utilizing a simple web interface for desktop and mobile devices. Features include downloading/uploading, renaming and removing items.

## Development
This project is in alpha-state.

## Running
### Dependencies
minCloud is written in Python3 and requires the [Tornado module](http://www.tornadoweb.org/) to be able to run the webserver.                                
You can install Tornado by using pip: ```sudo pip3 install tornado```.

### Configuration
Settings are stored in ```config.ini```.

```
[server]
port = your_port

[path]
store = path/to/storage

[auth]
key = generated_hash_key
username = admin_username
password = admin_password
```
The default port is set to ```9999``` and the default storage path is set to the ```cloudstore``` folder (located in the same directory as minCloud).

### Starting minCloud
Simply issue ```python mincloud.py``` through your command-line.

## License
minCloud is licensed under the [MIT](http://opensource.org/licenses/MIT) License.