# knossos_utils
A Python 3.x library for interacting with **KNOSSOS** datasets and annotation files.


# KnossosDataset

The KnossosDataset class can read data chunk-wise from datasets and .k.zips into NumPy arrays, or vice versa.

## Reading

A chunk is described by its offset into the dataset and its size, both specified in x,y,z order, and the desired magnification. The reading functions return numpy arrays in C-order, i.e. z,y,x. Per default, grayscale images are loaded as np.uint8 and segmentation as np.uint64.

```python
from knossos_utils import KnossosDataset

inp_dataset = KnossosDataset('/path/to/input_dataset_conf')

# loading a grayscale dataset chunk
raw_chunk = inp_dataset.load_raw(offset=(0, 0, 0), size=(1024, 512, 256), mag=1)
print(raw_chunk.shape) # output: (256, 512, 1024)

# loading the entire segmentation dataset
seg_chunk = inp_dataset.load_seg(offset=(0, 0, 0), size=inp_dataset.boundary, mag=1)

# loading segmentation from .k.zip annotation file. the region is specified by the movement_area inside the .k.zip
kzip_chunk = inp_dataset.load_kzip_seg(path='/path/to/segmentation.k.zip', mag=1)

# load a custom region from .k.zip:
kzip_chunk = inp_dataset._load_kzip_seg(path='/path/to/segmentation.k.zip', mag=1, offset=(0, 0, 0), size=(256,256,256))
```

## Writing

Writing a data chunk requires the z,y,x ordered numpy array to be written, the offset at which it should be saved and the chunk’s magnification. Per default KnossosDataset will automatically produce all other magnifications from it.

```python
out_dataset = KnossosDataset('/path/to/destination_dataset_conf')

out_dataset.save_raw(data=raw_chunk, data_mag=1, offset=(0, 0, 0))
out_dataset.save_seg(data=seg_chunk, data_mag=1, offset=(0, 0, 0))
out_dataset.save_to_kzip(data=kzip_chunk, data_mag=1, kzip_path='/write/destination.k.zip', offset=(0,0,0))
```

# Skeleton

A KNOSSOS skeleton is a graph structure with nodes and edges that are grouped into trees. This class can read skeletons from .k.zip or the legacy .nml format, but also import/export [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html).

## Basic Usage

```python
from knossos_utils.skeleton import Skeleton, SkeletonAnnotation, SkeletonNode

skel = Skeleton()
# loading from .k.zip or .nml
skel.fromNml('/path/to/input.k.zip')

# importing SWC
skel.fromSWC('/path/to/input.swc')

# iterating over nodes per tree
for tree: SkeletonAnnotation in skel.getAnnotations():
    for node: SkeletonNode in tree.getNodes():
        ...

# iterating over all nodes
for node: skeletonNode in skel.getNodes():
    ...

# saving
skel.to_kzip('/path/to/output.k.zip')

# exporting to SWC. Each tree will be saved as one SWC with the specified basename, e.g. /output/folder/prefix0.swc
skel.toSWC(basename='prefix', dest_folder='/output/folder')
```
