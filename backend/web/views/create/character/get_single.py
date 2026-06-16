from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character, Voice


class GetSingleCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            character_id = request.query_params.get('character_id')
            character = Character.objects.get(id=character_id, author__user=request.user)

            voices_raw = Voice.objects.order_by('id')
            voices = []
            for v in voices_raw:
                voices.append({
                    'id': v.id,
                    'name': v.name,
                })

            return Response({
                'result': 'success',
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'voice_id': character.voice.id if character.voice else None,
                },
                'voices': voices,
            })
        except Character.DoesNotExist:
            return Response({
                'result': '角色不存在或无权访问'
            })
        except Exception as e:
            return Response({
                'result': '系统异常，请稍后再试'
            })