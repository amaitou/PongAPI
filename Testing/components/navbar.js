
export function renderNavbar() {
  const header = document.getElementById('header');
  header.innerHTML = `
      <nav class="navbar navbar-expand-lg navbar-light p-3 d-flex" >
              <a class="navbar-brand" href="#">Ping Pong</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <form class="form-inline d-flex">
                <input class="form-control" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success ml-4" type="submit">Search</button>
             </form>
              <ul class="navbar-nav">
                  <li class="nav-item" style="font-size: 10px;">
                      <a class="nav-link" href="/signin">
                          <i class="fas fa-sign-out-alt" style="color: #dc3545;"></i> Logout
                      </a>
                  </li>
              </ul>
          </div>
      </nav>
  `;
}