package com.cs360.williambingham.bingham_william_c360_final_project.ui.login;

import android.arch.lifecycle.MutableLiveData;
import android.arch.lifecycle.ViewModel;
import com.cs360.williambingham.bingham_william_c360_final_project.data.LoginRepository;
import com.cs360.williambingham.bingham_william_c360_final_project.data.Result;
import com.cs360.williambingham.bingham_william_c360_final_project.data.model.LoggedInUser;
import com.cs360.williambingham.bingham_william_c360_final_project.R;

public class LoginViewModel extends ViewModel {

    private MutableLiveData<LoginResult> loginResult = new MutableLiveData<>();
    private LoginRepository loginRepository;

    LoginViewModel(LoginRepository loginRepository) {
        this.loginRepository = loginRepository;
    }

    public void login(String username, String password) {
        // can be launched in a separate asynchronous job
        Result<LoggedInUser> result = loginRepository.login(username, password);

        if (result instanceof Result.Success) {
            LoggedInUser data = ((Result.Success<LoggedInUser>) result).getData();
            loginResult.setValue(new LoginResult(new LoggedInUserView(data.getDisplayName())));
        } else {
            loginResult.setValue(new LoginResult(R.string.login_failed));
        }
    }
}
