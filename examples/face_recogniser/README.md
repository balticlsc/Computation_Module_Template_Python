# Face recogniser
Test the module in the following steps:
1. Prepare the config file that originally will be provided by BalticLSC system.
The listening below shows the example config:
```
[
	{
		"PinName": "Input",
		"PinType": "input",
		"AccessType": "",
		"DataMultiplicity": "single",
		"TokenMultiplicity": "single",
		"AccessCredential": {
			"User": "mongoadmin",
			"Password": "mongoadmin",
			"Host": "host.docker.internal",
			"Port": "27017"
		},
		"IsRequired": "true"
	},
	{
		"PinName": "Output",
		"PinType": "output",
		"AccessType": "",
		"DataMultiplicity": "single",
		"TokenMultiplicity": "single",
		"IsRequired": "false",
		"AccessCredential": {}
	}
]
```

2. Build and run the docker image. You can use [build_and_run](./build_and_run.sh) script. 
Make sure to provide proper config file directory using docker volume (see the script mentioned above).

3. Send an input token to the api.
The listening below shows the example token sending with the `curl` command:
    ```
    curl localhost:5000/token -X POST -H "Content-Type: application/json" -d 
   '{"msg_uid":"1", "pin_name":"Input", "values":"{\"Database\": \"test\", \"Collection\": \"images\", \"ObjectId\": \"6147283a675e72b966d0ee3a\"}", "access_type":"", "token_seq_stack": "[{\"seq_uid\": \"1\", \"no\": \"1\", \"is_final\": \"true\"}]"}'
   ```
