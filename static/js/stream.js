const APP_ID = 'AGORA_APP_ID'
const CHANNEL = sessionStorage.getItem('sala')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))





const client = AgoraRTC.createClient({mode: 'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async() => {
  //document.getElementById('nome_consulta').innerText = `Consulta nº ${CHANNEL}`
  let resposta = await fetch(`/get_user/?uid=${UID}`, {Cache: 'reload', credentials: 'include'})
  let dados = await resposta.json()
  let username = dados.username
  let nome = dados.nome
  let role = dados.role
  if (role != 'paciente'){
    nome = `${nome} (${role})`
  }
  client.on('user-published', handleUserJoined)
  client.on('user-left', handleUserLeft)

  UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)

  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

  let player = `<div class="card shadow mb-4" id="user-container-${UID}"><div class="card-header py-3"><h6 class="text-primary fw-bold m-0">${username}</h6></div>
                <div class="card-body  text-center shadow">
                    <div class="ratio ratio-4x3 video_stream" id="user-${UID}"></div><div class="mb-3"><p>${nome}</p></div>
                </div></div>`

  document.getElementById('video-streams').insertAdjacentHTML('afterbegin', player)

  localTracks[1].play(`user-${UID}`)

  await client.publish([localTracks[0], localTracks[1]])

}



let handleUserJoined = async (user, mediaType) => {
  let resposta = await fetch(`/get_user/?uid=${user.uid}`, {Cache: 'reload', credentials: 'include'})
  let dados = await resposta.json()
  let username = dados.username
  let nome = dados.nome
  let role = dados.role
  if (role != 'paciente'){
    nome = `${nome} (${role})`
  }

  remoteUsers[user.uid] = user
  await client.subscribe(user, mediaType)

  if(mediaType === 'video'){
    let player = document.getElementById(`user-container-${user.uid}`)
    if(player != null){
      player.remove()
    }

    player = `<div class="card shadow mb-4" id="user-container-${user.uid}"><div class="card-header py-3"><h6 class="text-primary fw-bold m-0">${username}</h6></div>
                  <div class="card-body  text-center shadow">
                      <div class="ratio ratio-4x3 video_stream" id="user-${user.uid}"></div><div class="mb-3"><p>${nome}</p></div>
                  </div></div>`

    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    user.videoTrack.play(`user-${user.uid}`)


  }

  if(mediaType === 'audio'){
      user.audioTrack.play()

  }
}

let handleUserLeft = async(user) => {
  delete remoteUsers[user.uid]
  document.getElementById(`user-container-${user.uid}`).remove()
}
