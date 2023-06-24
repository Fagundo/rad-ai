# rad-ai
Coding exercise for Rad AI

# Summary
The summarization service has one endpoint `/summary`, which takes a POST request with the following fields in the json payload

- text (str): Text to summarize
- summary_lenght (int): Maximum word count for the summary.

The service uses the `facebook/bart-large-cnn` model from Hugging Face, which is loaded during the docker build. 

For instructions on how to run and test, please see below...

# How To
## Build
To build to dockerfile, simply run `docker build -t radai .`

Please note that the Hugging Face summarization model will be downloaded at this step. This allows us to download it once for the container, rather than every time we initialize the container. Accordingly, the entire build process should take roughly 7 minutes.

## Run
After building the container, run the service with the following command `docker run -d -p 8000:8000 radai`

- The service will take a POST request at `/summary` to return a json response of `{summary: <summary>}`
- The request must have the following features:
    - text (str): Text to summarize
    - summary_lenght (int): Maximum word count for the summary. Minimum is 10, max is 498.

## Test
A test script is offered to generate summaries. Once the docker container has loaded, navigate to the repo's `test` folder. 

Run the test with `python3 post.py` to see the summary for a given preloaded article.

If you would like to pass your own article and word count, save the article to a file. The request can be done with the following command `python3 post.py -f <file_path> -l <summary_length>`

# Questions
## Scaling training while maintain reasonable speed, cost and size trade offs.
- To increase model experimentation rate, one could package the model training within a docker container and deploy to SageMaker training jobs. Accordingly, one could sweep across model parameters to find the optimal hyperparameters for model quality while minimizing overall training time. 
- Part of the above solution would involve sweeping across architecture sizes. You could set an acceptable model performance metric value, and try a number of model sizes (for the transformer, the number of stacked encoder-decoder blocks, key-query-value size) while holding other parameters equal. The smallest model that meets the above criteria can then be used for further hyperparameter tuning. As a result, the smaller model will afford both shorter training times, a smaller size and provide cost savings in further training iterations. 
- If cloud computing costs are a concern, it is always cost effective to use an on-prem server for the final model training. One could choose a subset of data and models to train for identifying optimal hyperparameters via a sweep in the cloud. Using a smaller subset of data would provide time and cost savings while revealing reliable hyperparameter values. Once a viable model and parameters are selected, you would train the optimal model on the entire dataset on a local server to provide cost savings.

## Inference optimization
I would take a multistage approach in optimizing model inference.

1. Regarding maintaining speed / size tradeoff, I would create a unique test set to benchmark against. Whenever a new model is trained, a step in the MLOps pipeline would benchmark the model's speed by inferring against the preset corpus of test samples. One would compute inference time normalized in some way by size (perhaps sample_inference_time / sample_size). The final benchmark value for the model would be the upper limit of the 95% confidence interval for normalized inference time across samples. If this meets a certain threshold, we can be confident in deploying this size model while maintaining appropriate inference speeds.
2. Minimizing latency would involve both architectural, postprocessing and deployment decisions. For architectural design, the solution would be to identify the optimal size that lowers latency while maintaining viable test scores. There are a few additional options for postprocessing the model, including quantization and model pruning. A step in the MLOps pipeline could apply these steps after training. The post-processed model could be run against the test set in order to infer any degredation in loss and gain in speed. If the speed/quality trade off is acceptable, the model can be further deployed into the field. Finally, there are choices around deployment that impact speed. For example, the types of instances the model is deployed do (not all GPUs are created equal), the architectural decisions for the api service, as well as the number of instances created for serving. For a dynamic system, I would recommend creating a cloud deployment that scales according to demand (akin to AWS Fargate). In this way, you can have as many deployments as possible during peak demand, and save on costs when the system has light use.
