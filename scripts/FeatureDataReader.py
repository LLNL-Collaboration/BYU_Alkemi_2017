import numpy as np
import sys

class FeatureDataReader:

    def __init__(self, dataDir, numParts):
        self._dataDir = dataDir
        self._numParts = numParts
        
        self._zoneOffsets = {}
        self._indexCache = {}
        self._metaData = {}
        

    #################### Public Members ####################

    def readZone(self, run, cycle, zone):
        zid = self._getZoneOffset(zone)

        index = self._readFileIndex(run, zid['part'])
        meta = self._readMetaData(zid['part'])
        
        fname = '%s/features/features_p%02d_r%03d.npy' % (self._dataDir, zid['part'], run)
        nmetrics = len(meta['metrics'])
        offset = zid['offset'] * nmetrics * 4

        with open(fname, 'rb') as fin:
            fin.seek(index[cycle] + offset)
            return np.fromfile(fin, dtype=np.float32, count=nmetrics)


    def readPartition(self, run, part, cycle):
        index = self._readFileIndex(run, part)
        meta = self._readMetaData(part)

        fname = '%s/features/features_p%02d_r%03d.npy' % (self._dataDir, part, run)
        nmetrics = len(meta['metrics'])
        nzones = len(meta['zones'])
        
        with open(fname, 'rb') as fin:
            fin.seek(index[cycle])
            data = np.fromfile(fin, dtype=np.float32, count=nzones*nmetrics)
            return np.reshape(data, (nzones,nmetrics))


    def readAllCyclesForZone(self, run, zone):
        zid = self._getZoneOffset(zone)

        index = self._readFileIndex(run, zid['part'])
        meta = self._readMetaData(zid['part'])
        
        fname = '%s/features/features_p%02d_r%03d.npy' % (self._dataDir, zid['part'], run)
        nmetrics = len(meta['metrics'])
        offset = zid['offset'] * nmetrics * 4

        with open(fname, 'rb') as fin:
            data = []
            for cycle in sorted(index.keys()):
                fin.seek(index[cycle] + offset)
                single = np.fromfile(fin, dtype=np.float32, count=nmetrics)
                data.append(np.reshape(single, (1,nmetrics)))
            return np.concatenate(data)


    def readAllZonesInCycle(self, run, cycle):
        data = []
        for part in range(0, self._numParts):
            data.append(self.readPartition(run, part, cycle))
        return np.concatenate(data)


    def getPartitionZoneIds(self, part):
        meta = self._readMetaData(part)
        return np.asarray(meta['zones'].keys(), dtype=np.int32)


    def getCycleZoneIds(self):
        data = []
        for part in range(0, self._numParts):
            data.append(self.getPartitionZoneIds(part))
        return np.concatenate(data)


    #################### Private Members ####################

    def _readFileIndex(self, run, part):
        fname = '%s/indexes/indexes_p%02d_r%03d.txt' % (self._dataDir, part, run)

        if fname not in self._indexCache:
            with open(fname, 'r') as fin:
                index = {}
                for line in fin:
                    key,val = line.split(' -> ')
                    index[int(key)] = int(val)

                self._indexCache[fname] = index
        return self._indexCache[fname]


    def _readMetaData(self, part):
        fname = '%s/features/metadata_p%02d.txt' % (self._dataDir, part)

        if fname not in self._metaData:
            with open(fname, 'r') as fin:
                fin.readline()  # skip metrics header

                names = fin.readline().rstrip('\n').split(',')
                metrics = dict(zip(names, range(0, len(names))))

                fin.readline()  # skip zones header

                ids = fin.read().splitlines()
                zones = dict(zip(map(int, ids), range(0, len(ids))))

                self._metaData[fname] = {'metrics': metrics, 'zones': zones}
        return self._metaData[fname]


    def _getZoneOffset(self, zone):
        if not self._zoneOffsets:
            for part in range(0, self._numParts):
                meta = self._readMetaData(part)

                for key in meta['zones'].keys():
                    self._zoneOffsets[key] = {'part': part, 'offset': meta['zones'][key]}
        return self._zoneOffsets[zone]


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: FeatureDataReader.py dataDir numParts"
        sys.exit(1)

    reader = FeatureDataReader(sys.argv[1], int(sys.argv[2]))

    np.set_printoptions(suppress=True, precision=4)

    data = reader.readZone(0, 0, 0)
    print data

    data = reader.readPartition(0, 0, 0)
    print data.shape

    data = reader.readAllZonesInCycle(0, 0)
    print data.shape

    data = reader.readAllCyclesForZone(0, 0)
    print data.shape

    data = reader.getPartitionZoneIds(0)
    print data.shape
    
    data = reader.getCycleZoneIds()
    print data.shape
    
