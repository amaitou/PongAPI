export function rendercontent() 
{

  console.log("contentHome");
  const header = document.getElementById('content');
  header.innerHTML += `
  <div class="col" style="font-family: Arial, Helvetica, sans-serif;"> 
  <div class="m-4">
    <h1 class="h4 mb-0">Hello <span class="text-primary">Solix!</span></h1>
                <p class="mb-0">Ready for a gaming surprise? Click 'Play' to start a random game.</p>
    </div>
  <!-- Game Modes -->
  <div class="row m-5">
      <div class="col-lg-3 m-3">
          <div class="card text-center p-4">
              <img src="https://placehold.co/100x100" class="card-img-top mx-auto" alt="Classic Mode">
              <div class="card-body">
                  <h5 class="card-title">CLASSIC</h5>
                  <p class="card-text">Play a game of ping pong</p>
                  <a href="#" class="btn btn-primary">Play now</a>
              </div>
          </div>
      </div>
      <div class="col-lg-4 m-3">
          <div class="card text-center p-4">
              <img src="https://placehold.co/100x100" class="card-img-top mx-auto" alt="AI Mode">
              <div class="card-body">
                  <h5 class="card-title">AI MODE</h5>
                  <p class="card-text">Challenge the computer</p>
                  <a href="#" class="btn btn-primary">Play now</a>
              </div>
          </div>
      </div>
      <div class="col-lg-3 m-3">
          <div class="card text-center p-4">
              <img src="https://placehold.co/100x100" class="card-img-top mx-auto" alt="Friends Mode">
              <div class="card-body">
                  <h5 class="card-title">FRIENDS MODE</h5>
                  <p class="card-text">Beat your friends in 1 vs 1</p>
                  <a href="#" class="btn btn-primary">Play now</a>
              </div>
          </div>
      </div>
  </div>

  <!-- Best Players -->
  <div class="m-4">
      <h3 class="mb-3">Best Players</h3>
      <div class="row">
          <!-- Player 1 -->
          <div class="col-lg-6 mb-3">
              <div class="bestplayer d-flex justify-content-between align-items-center  m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 1" class="rounded-circle me-3">
                      <strong>KAMAZLI</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2540PTS</span>
                      <span class="badge bg-success">9.2</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 1" class="rounded-circle me-3">
                      <strong>KAMAZLI</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2540PTS</span>
                      <span class="badge bg-success">9.2</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 1" class="rounded-circle me-3">
                      <strong>KAMAZLI</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2540PTS</span>
                      <span class="badge bg-success">9.2</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 1" class="rounded-circle me-3">
                      <strong>KAMAZLI</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2540PTS</span>
                      <span class="badge bg-success">9.2</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 1" class="rounded-circle me-3">
                      <strong>KAMAZLI</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2540PTS</span>
                      <span class="badge bg-success">9.2</span>
                  </div>
              </div>
          </div>
          <!-- Player 2 -->
          <div class="col-lg-6 mb-3">
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 2" class="rounded-circle me-3">
                      <strong>MOSSCLEF</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2320PTS</span>
                      <span class="badge bg-success">9.0</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 2" class="rounded-circle me-3">
                      <strong>MOSSCLEF</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2320PTS</span>
                      <span class="badge bg-success">9.0</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 2" class="rounded-circle me-3">
                      <strong>MOSSCLEF</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2320PTS</span>
                      <span class="badge bg-success">9.0</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 2" class="rounded-circle me-3">
                      <strong>MOSSCLEF</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2320PTS</span>
                      <span class="badge bg-success">9.0</span>
                  </div>
              </div>
              <div class="bestplayer d-flex justify-content-between align-items-center m-2 p-2 rounded">
                  <div class="d-flex align-items-center">
                      <img src="https://placehold.co/40x40" alt="Player 2" class="rounded-circle me-3">
                      <strong>MOSSCLEF</strong>
                  </div>
                  <div class="d-flex align-items-center">
                      <span class="me-3">2320PTS</span>
                      <span class="badge bg-success">9.0</span>
                  </div>
              </div>
          </div>
          <!-- Player 3, 4, etc. -->
      </div>
  </div>
</div>

<!-- Recent Activity -->
<aside class="col-lg-3">
  <div class="card m-4 p-3">
      <div class="d-flex align-items-center mb-3">
          <img src="https://placehold.co/64x64" alt="Profile" class="rounded-circle me-3">
          <div>
              <h4 class="card-title">My Profile</h4>
              <p class="mb-0">SOLIX</p>
              <p class="mb-0">Level 6.18</p>
              <p class="text-success">+120PTS</p>
          </div>
      </div>
      <p>Last Game: <strong>Won</strong></p>
      <p>Status: <strong>Offline</strong></p>
  </div>

  <div class="activity card m-4 p-3">
      <h4 class="card-title mb-3">Recent Activity</h4>
      <div class="d-flex justify-content-between mb-3">
          <button class="btn btn-outline-light btn-sm">All</button>
          <button class="btn btn-outline-light btn-sm">Friends</button>
      </div>
      <ul class="list-unstyled">
          <li class="d-flex justify-content-between mb-2">
              <span>frankfurter won against schoukous</span>
              <span class="text-muted">10:21 AM</span>
          </li>
          <li class="d-flex justify-content-between mb-2">
              <span>mossclef won against tchaibi</span>
              <span class="text-muted">09:30 AM</span>
          </li>
          <!-- Other activity logs -->
      </ul>
  </div>
</aside>
  `;
}