# Pandora (BETA)
Export Maltego Graphs to JSON format  
This means you can import them into Splunk, ElasticSearch or anything else that accepts JSON  

  
# Command Line Export  
To run a simple export you can use the command line as below  
*./pandora ExampleGraph.mtgz*  
This will save the new json file to *output/ExampleGraph.json*  
  
# Web Interface  
You can also use the web interface to export and view the output. To start the web server just run:  
*./webserver.py*  
This will start a small Flask web server on port 5000  
  
This is just the beginning of the project so more updates will come. 
