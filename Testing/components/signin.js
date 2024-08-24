export function renderSignIn()
{
const signup = document.getElementById('body');
signup.innerHTML=`
  <div class="d-flex align-items-center justify-content-center vh-100">
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h2 class="text-center" style="color:#ffff;">Sign In</h2>
                <form id="signInForm" action="/profile" method="GET" style="font-family: 'Fantasy', cursive;">
                    <div class="mb-3">
                        <label for="username" class="form-label" style="color:#ffff;">Username</label>
                        <input type="text" class="form-control" id="username" required>
                    </div>
                    <div class="mb-3">
                      <label for="password" class="form-label" style="color:#ffff;">Password</label>
                      <input type="password" class="form-control" id="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 mt-2">Sign In</button>
                </form>
            </div>
        </div>
    </div>
  </div>
`
}