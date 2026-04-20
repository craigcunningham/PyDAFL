from DAFLDraft.models import Team


def teams_processor(request):
    teams = Team.objects.all()
    logos = ["", "butjustice.jpg", "sadsacks.jpg", "oxy.jpg", 
          "ncp2.jpg", "nachohelmet.jpg", "shooters.jpg", "BandD.jpg", 
          "plankton.jpg", "tetras.jpg", "homers.jpg",   
          "fluffy.jpg", "heroes.jpg",
          "chrismom.jpg", "cricket2.jpg"]        
    return {'teams': teams, 'teamlogos': logos}