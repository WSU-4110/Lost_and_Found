public class User {
    private String username;
    private String password;
    private String email;
    private String name;

    public User(String username, String password, String email, String name) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.name = name;
    }

    public void setUsername(String username) {
        this.username = username;
    }
    public String getUsername() {
        return this.username;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public String getPassword() {
        return this.password;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public String getEmail() {
        return this.email;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return this.name;
    }

}

interface Authentication_Strategy {
    boolean checkLogin(User user);
    boolean validateUser(User user);
    boolean validatemail(String email);
}


class loginauth implements Authentication_Strategy {
    @Override
    public boolean checkLogin(User user) {  
        //implement login check
        return false;
    }

    @Override
    public boolean validateUser(User user) {
       //implement user validation check    
        return true;
    }

    @Override
    public boolean validatemail(String email) {
        //implement email validation check
        return true;
    }
}
class signupauth implements Authentication_Strategy {
    @Override
    public boolean checkLogin(User user) {
        //implement login check
        return false;
    }

    @Override
    public boolean validateUser(User user) {
       //implement user validation check    
        return true;
    }

    @Override
    public boolean validatemail(String email) {
        //implement email validation check
        return email.endsWith("@wayne.edu");
    }
}
