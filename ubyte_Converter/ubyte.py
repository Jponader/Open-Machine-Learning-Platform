import gzip
import numpy as np


def readUbyteImages(filename):
	f = gzip.open(filename, "rb")
	data = f.read(16)
	dt = dataType(data[2])

	if data[3] == 0x03:
		k = 1
	elif data[3] == 0x04:
		k = nt.from_bytes(f.read(4), byteorder='big', signed=True)
	else:
		assert True, "Input Not Images"

	x = int.from_bytes(data[4:8], byteorder='big', signed=True)
	y = int.from_bytes(data[8:12], byteorder='big', signed=True)
	z = int.from_bytes(data[12:], byteorder='big', signed=True)

	buf = f.read(x * y * z * k)
	data = np.frombuffer(buf, dtype=dt).astype(np.float32)
	data = data.reshape(x, y, z, k)

	return data

def readUbyteLabels(filename):
	f = gzip.open(filename, "rb")
	data = f.read(8)
	dt = dataType(data[2])

	assert data[3] == 0x01, "Input Not Labels"

	x = int.from_bytes(data[4:8], byteorder='big', signed=True)

	buf = f.read(x)
	data = np.frombuffer(buf, dtype=dt).astype(np.float32)
	data = data.reshape(x,1)

	return data


# 0x08: unsigned byte
# 0x09: signed byte
# 0x0B: short (2 bytes)
# 0x0C: int (4 bytes)
# 0x0D: float (4 bytes)
# 0x0E: double (8 bytes)
def dataType(num):
	if num == 0x08:
		return np.uint8
	if num == 0x09:
		return np.int8
	if num == 0x0B:
		return np.uint16
	if num == 0x0C:
		return np.int32
	if num == 0x0D:
		return np.float32
	if num == 0x0E:
		return np.float64 

	assert False, "Not Data Type"


def main():
	data = readUbyteImages("sampleData/t10k-images-idx3-ubyte.gz")
	import matplotlib.pyplot as plt
	image = np.asarray(data[10]).squeeze()
	plt.imshow(image)
	plt.show()
	data = readUbyteLabels("sampleData/t10k-labels-idx1-ubyte.gz")
	

if __name__ == '__main__':
    main()