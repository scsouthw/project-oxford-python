from .Base import Base

_faceListUrl = 'https://api.projectoxford.ai/face/v1.0/facelists'


class FaceList(Base):
    """Client for using the Project Oxford Face List APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def addFace(self, faceListId, options, targetFace=None, userData=None):
        """Adds a face to a Face list.
        The face ID must be added to a person before its expiration. Typically a face ID expires
        24 hours after detection.

        Args:
            faceListId (str). The target person's person group.
            targetFace (str). The target person that the face is added to.
            options (object). The Options object
            options.url (str). The URL to image to be used
            options.path (str). The Path to image to be used
            options.stream (stream). The stream of the image to be used
            userData (str).  Optional. Attach user data to person's face. The maximum length is 1024.

        Returns:
            object. The resulting JSON
        """
        params = {
            'faceListId' : faceListId
        }

        if targetFace is not None:
            params['targetFace'] = targetFace
                    
        if userData is not None:
            params['userData'] = userData

        uri = _faceListUrl + '/' + faceListId + '/persistedFaces'
        
        return Base._postWithOptions(self, uri, options, params)

    def deleteFace(self, faceListId, persistedFaceId):
        """Deletes a face from a person.

        Args:
            faceListId (str). The target person's person group.
            persistedFaceId (str). The target person that the face is removed from.

        Returns:
            object. The resulting JSON
        """

        uri = _faceListUrl + '/' + faceListId + '/persistedFaces/' + persistedFaceId
        return self._invoke('delete', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def update(self, faceListId, name, userData=None):
        """Updates a face for a person.

        Args:
            faceListId (str). The target person's person group.
            name (str). Target face list display name. The maximum length is 128.
            userData (str). Optional fields for user-provided data attached to a person. Size limit is 16KB.


        Returns:
            object. The resulting JSON
        """

       	body = {
            'name': name
        }

        if userData is not None:
            body['userData'] = userData
            
        uri = _faceListUrl + '/' + faceListId
        return self._invoke('patch', uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def create(self, faceListId, name, userData=None):
        """Creates a new facelist.
        The number of faces has a subscription limit. Free subscription amount is 1000 faces.
        The maximum number of face lists is 64.

        Args:
            name (str). Target person's display name. The maximum length is 128.
            userData (str). Optional fields for user-provided data attached to a person. Size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name,
            'userData': userData
        }

        return self._invoke('put',
                            _faceListUrl + '/' + faceListId,
                            json=body,
                            headers={'Ocp-Apim-Subscription-Key': self.key})
                            

    def delete(self, faceListId):
        """Deletes an existing Face List.

        Args:
            faceListId (str). The target face list id.

        Returns:
            object. The resulting JSON
        """

        uri = _faceListUrl + '/' + faceListId
        return self._invoke('delete', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def get(self, faceListId):
        """Gets an existing Face List.

        Args:
            faceListId (str). The target face list id.

        Returns:
            object. The resulting JSON
        """
        return self._invoke('get',
                            _faceListUrl + '/' + faceListId,
                            headers={'Ocp-Apim-Subscription-Key': self.key})


    # def createOrUpdate(self, personGroupId, faceIds, name, userData=None):
    #     """Creates or updates a person's information.

    #     Args:
    #         personGroupId (str). The target person's person group.
    #         faceIds ([str]). Array of face id's for the target person.
    #         name (str). Target person's display name. The maximum length is 128.
    #         userData (str). Optional fields for user-provided data attached to a person. Size limit is 16KB.

    #     Returns:
    #         object. The resulting JSON
    #     """
    #     persons = self.list(personGroupId)
    #     for person in persons:
    #         if person['name'] == name:
    #             self.update(personGroupId, person['personId'], faceIds, name, userData)
    #             return person

    #     return self.create(personGroupId, faceIds, name, userData)

    def list(self):
        """List Face Lists.

        Returns:
            object. The resulting JSON
        """

        uri = _faceListUrl
        return self._invoke('get', uri, headers={'Ocp-Apim-Subscription-Key': self.key})
