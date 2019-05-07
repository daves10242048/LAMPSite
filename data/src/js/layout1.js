//// use "simplecookie.js"

function logout()
{
    let logout_error = null;

    $.ajax({
        url: '/ajax/logout-ajax.py',
        timeout: 10000,
        type: 'post',
        datatype: 'text',
        data: {
            token: SimpleCookies.get('temp_token')
        },
        success: function(response)
        {
            try {
                if (logout_error) return;

                if (response.startsWith('ERROR --')) {
                    logout_error = response;
                    throw response;
                }

                window.location.href = '/logout.py';
            } catch (exc) {
                if (exc.trim() === 'ERROR -- You are already logged out.') {
                    window.location.href = '/logout.py?error=1';
                } else if (exc.trim() === 'ERROR -- Invalid token.') {
                    window.location.href = '/logout.py?error=2';
                } else {
                    window.location.href = '/logout.py?error=0';
                }
            }
        },
        error: function(request, status, err)
        {
            try {
                if (status == 'timeout') {
                    logout_error = 'ERROR -- Request timed out.';
                    throw logout_error;
                } else {
                    logout_error = 'ERROR -- ' + err;
                    throw logout_error;
                }
            } catch (exc) {
                alert(exc);
            }
        }
    });

    return false;
}