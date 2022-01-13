# Installing platypus on Kubernetes

You can follow these instructions to install platypus in a Kubernetes cluster provisioned through a cloud provider or running in an on-premises environment. Supported cloud providers are Amazon Elastic Kubernetes Service (EKS), Google Kubernetes Engine (GKE), and Microsoft Azure Kubernetes Service (AKS).


## Prerequisites

* Ensure that you have an existing Kubernetes cluster.
* Ensure that Helm 3 is set up on a local machine.
* Ensure that a local kubectl is configured to access your Kubernetes cluster.

## Procedure

1. Download [the `platypus-cloud-tools` repository](https://github.com/duckbills/platypus-cloud-tools).
1. In a terminal window, change to the `platypus-cloud-tools/charts/platypus/` directory.
1. Review the default values in the file `values.yaml`, which configures the platypus installation. If you want to override any of these values, create a file with the `.yaml` extension in this directory, copy into this file the keys for which you want to set non-default values, and then set the values in the file. Making changes in this file allows you to quickly update to the latest version of the chart by copying the file across Helm chart updates. Refer to "[`values.yaml` Reference](./docs/Values-Reference.md)" for details about the settings.
1. Install the Helm Chart by running one of these commands from the `charts` directory:
   * If you are overriding any of the default values that are in the `values.yaml` file, run this command:

      ```bash
      $ helm install <release-name> platypus -f <file>
      ```
      where `<file>` is the name of the file that you are using to override values.
   * If you are not overriding any of the values in the `values.yaml` file, run this command:
      ```bash
      $ helm install <release-name> platypus
      ```

   If the installation takes longer than a few minutes to complete, you can check the status of the installation by using the following command:

   ```bash
   $ kubectl get pods
   ```

   If a pod remains in **Pending** state for more than a few minutes, run the following command to view its status to check for issues, such as insufficient resources for scheduling:

   ```bash
   $ kubectl describe pods <pod-name>
   ```

   If the events at the bottom of the output mention insufficient CPU or memory, either adjust the values in your `values.local.yaml` and restart the process or add more resources to your Kubernetes cluster.

   When all of the pods are in the **Ready** state, the installation is complete.

## What to do next

Now that you've installed the platypus Helm chart, you can get the  addresses for connecting to platypus's primary and replica

   ```bash
   $ kubectl get service  
   ```


### Getting the HTTP address for connecting to the platypus servers 


```
$ kubectl get services
```

* If the value in the `TYPE` column of the output is `LoadBalancer`, access the platypus servers through the address in the `EXTERNAL_IP` column and port 8900.
For example, in the output below, the value under the `EXTERNAL-IP` column is 192.168.49.1. Therefore, you can get to the platypus-primary via port 8900 on that address: http://10.105.39.12:9047
   ```
   $ kubectl get services
  
   NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)                          AGE
   myplatypus-primary   LoadBalancer   10.105.39.12    192.168.49.11   8900:31006/TCP   2m25s
   myplatypus-replica   LoadBalancer   10.99.173.172   192.168.49.10   9900:30003/TCP   2m25s

   ```
