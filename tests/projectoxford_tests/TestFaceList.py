import inspect
import os
import sys
import unittest
import uuid
import copy

rootDirectory = os.path.dirname(os.path.realpath('__file__'))
if rootDirectory not in sys.path:
    sys.path.append(os.path.join(rootDirectory, '..'))

from test import test_support
from projectoxford.Client import Client

class TestFaceList(unittest.TestCase):
    '''Tests the project oxford API client'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Client(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        cls.face1 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face1.jpg')})[0]
        cls.face2 = cls.client.face.detect({'path': os.path.join(cls.localFilePrefix, 'face2.jpg')})[0]
        cls.knownFaceIds.append(cls.face1['faceId'])
        cls.knownFaceIds.append(cls.face2['faceId'])
        
    def test_face_list_create_delete(self):
        faceListId = str(uuid.uuid4())
        result = self.client.face.faceList.create(faceListId, 'python-test-facelist', 'test-data')
        self.assertIsNone(result, "empty response expected")
        self.client.face.faceList.delete(faceListId)

    def test_face_list_list(self):
        faceListId = str(uuid.uuid4())
        self.client.face.faceList.create(faceListId, 'python-test-group', 'test-data')
        result = self.client.face.faceList.list()
        match = next((x for x in result if x['faceListId'] == faceListId), None)
        self.assertEqual(match['faceListId'], faceListId)
        self.assertEqual(match['name'], 'python-test-group')
        self.assertEqual(match['userData'], 'test-data')
        self.client.face.faceList.delete(faceListId)

    def test_face_list_get(self):
        faceListId = str(uuid.uuid4())
        response = self.client.face.faceList.create(faceListId, 'python-test-group', 'test-data')
        result = self.client.face.faceList.get(faceListId)
        self.assertEqual(result['faceListId'], faceListId)
        self.assertEqual(result['name'], 'python-test-group')
        self.assertEqual(result['userData'], 'test-data')
        self.client.face.faceList.delete(faceListId)

    def test_face_list_update(self):
        faceListId = str(uuid.uuid4())
        self.client.face.faceList.create(faceListId, 'python-test-group', 'test-data')
        result = self.client.face.faceList.update(faceListId, 'python-test-group2', 'test-data2')
        self.assertIsNone(result, "empty response expected")
        
        result = self.client.face.faceList.get(faceListId)
        self.assertEqual(result['faceListId'], faceListId)
        self.assertEqual(result['name'], 'python-test-group2')
        self.assertEqual(result['userData'], 'test-data2')
        
        self.client.face.faceList.delete(faceListId)

    def test_face_list_add_delete_face(self):
        faceListId = str(uuid.uuid4())
        self.client.face.faceList.create(faceListId, 'python-test-group', 'test-data')
        faceRect = self.face1['faceRectangle']
        target = "%s,%s,%s,%s" % (faceRect['left'], faceRect['top'], faceRect['width'], faceRect['height'])
        result = self.client.face.faceList.addFace(faceListId, {'path': os.path.join(self.localFilePrefix, 'face1.jpg')}, targetFace=target, userData="Test Face Target")
        self.assertIsNotNone(result['persistedFaceId'])        
        
        persistedFaceId = result['persistedFaceId']
        result = self.client.face.faceList.deleteFace(faceListId, persistedFaceId)
        self.assertIsNone(result)