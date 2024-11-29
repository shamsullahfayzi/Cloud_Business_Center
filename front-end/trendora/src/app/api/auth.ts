import apiClient from "./api"
export type Login_type = {
    email: string
    password: string
    role: number
}
export type Login_response = {
    success: boolean
    message: string
}
const login = async (login: Login_type) => {
    const res = await apiClient.post("login/", login)
    if (res.status == 401) {
        const login_res: Login_response = {
            success: false,
            message: "Invalid email or password"
        }
        return login_res

    }
    else if (res.status == 200) {
        const login_res: Login_response = {
            success: true,
            message: `welcome back`
        }
        return login_res

    }
    const login_res: Login_response = {
        success: false,
        message: "An unexpected error has occurred"
    }
    return login_res
}
export default login
