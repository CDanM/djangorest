from rest_framework import permissions
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import mixins
from rest_framework import generics
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


class SnippetList(generics.ListCreateAPIView):

  """
  List all snippets,or create a new snippet.
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

@api_view(('GET',))
def api_root(request, format=None):
  return Response({
    'users':reverse('users-list', request=request, format=format),
    'snippets': reverse('snippet-list',request=request,format=format)
    })

class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = (renderers.StaticHTMLRenderer,)

  def get(self, request, *args, **kwargs):
      snippet = self.get_object()
      return Response(snippet.highlighted)
