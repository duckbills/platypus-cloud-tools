# `Values.yaml` Reference

🔎 To search this document for specific values, use dot-notation to search, i.e. `coordinator.volumeSize`.

ℹ️ In all code examples, `[...]` denotes additional values that have been omitted.

## Top Level Values

### Image Configuration

#### `image`

Type: String

By default, the image is set to `platypus/platypus-oss`, the community edition of platypus.

The `image` refers to the location to retrieve the specific container image for platypus. In some cases, the `image` value may vary in corporate environments where there may be a private container registry that is used.

#### `imageTag`

Type: String

By default, the value is set to `latest`.

It is **strongly** recommended to pin the version of platypus that we are deploying by setting the `imageTag` to a precise version and not leave the value as latest. Since platypus versions are not backwards compatible, leaving it as latest may automatically upgrade platypus during pod creation.

#### `imagePullSecrets`

Type: Array

By default, this value is not set.

In some environments, an internal mirror may be used that requires authentication. For enterprise users, you may need to specify the `imagePullSecret` for the Kubernetes cluster to have access to the platypus enterprise image. Please refer to the documentation [Pull an Image from a Private Repository](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) provided by Kubernetes on how to create an image pull secret.


### Kubernetes Service Account

#### `serviceAccount`

Type: String

By default, this value is not set and will use the default service account configured for the Kubernetes cluster.

This value is independently overridable in each section ([`primary`](#primary), [`replica`](#replica)).

More Info: See the [Service Accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) documentation for Kubernetes.

### Storage Configuration

#### `storageClass`

Type: String

By default, this value is not set and will use the default storage class configured for the Kubernetes cluster.

Storage class has a direct impact on the performance of the platypus cluster. Optionally set this value to use the same storage class for all persistent volumes created. This value is independently overridable in each section ([`primary`](#primary), [`replica`](#replica)).

More Info: See the [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) documentation for Kubernetes.

### Annotations, Labels, Node Selectors, Tags, and Tolerations

By default, these values are set to empty. These values are independently overridable in each section ([`primary`](#primary), [`replica`](#replica)).

#### `annotations`

Type: Dictionary

The annotations set at this root level are used by all `StatefulSet` resources unless overridden in their respective configuration sections.

For example, you can set annotations as follows:

```yaml
annotations:
  example-annotation-one: "example-value-one"
  example-annotation-two: "example-value-two"
[...]
```

More Info: See the [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) documentation for Kubernetes.

#### `podAnnotations`

Type: Dictionary

The pod annotations set at this root level are used by all `Pod` resources unless overridden in their respective configuration sections.

For example, you can set pod annotations as follows:

```yaml
podAnnotations:
  example-pod-annotation-one: "example-value-one"
  example-pod-annotation-two: "example-value-two"
[...]
```

More Info: See the [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) documentation for Kubernetes.

#### `labels`

Type: Dictionary

The labels set at this root level are used by all `StatefulSet` resources unless overridden in their respective configuration sections.

For example, you can set labels as follows:

```yaml
labels:
  example-label-one: "example-value-one"
  example-label-two: "example-value-two"
[...]
```

More Info: See the [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) documentation for Kubernetes.

#### `podLabels`

Type: Dictionary

The pod labels set at this root level are inherited by all `Pod` resources unless overridden in their respective configuration sections.

For example, you can set pod labels as follows:

```yaml
podLabels:
  example-pod-label-one: "example-value-one"
  example-pod-label-two: "example-value-two"
[...]
```

More Info: See the [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) documentation for Kubernetes.

#### `nodeSelector`

Type: Dictionary

The node selectors set at this root level are inherited by all `Pod` resources unless overridden in their respective configuration sections.

For example, you can set the node selector to select nodes that have a label `diskType` of value `ssd` as follows:

```yaml
nodeSelector:
  diskType: "ssd"
[...]
```

More Info: See the [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) section of Assigning Pods to Nodes documentation for Kubernetes.

#### `tolerations`

Type: Array

The tolerations set at this root level are inherited by all `Pod` resources unless overridden in their respective configuration sections.

For example, if there is a node with the taint `example-key=example-value:NoSchedule`, you can set the tolerations to allow the pod to be scheduled as follows:

```yaml
tolerations:
- key: "example-key"
  operator: "Exists"
  effect: "NoSchedule"
[...]
```

More Info: See the [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) documentation for Kubernetes.

### platypus Configuration

#### `primary`

Type: Dictionary

This section controls the deployment of primary instance(s). See the [Primary Values](#primary-values) section.

#### `replica`

Type: Dictionary

This section controls the deployment of executor instance(s). See the [Replica Values](#replica-values) section.


