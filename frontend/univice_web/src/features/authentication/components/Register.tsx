import { useState } from "react";
import {
    Search,
    ChevronRight,
    GraduationCap,
    Pencil,
    Users,
    Mail,
} from "lucide-react";


export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    return (
        <div className="min-h-screen bg-gradient-to-b from-white flex items-center justify-center px-4 py-10">
            <div className="w-full max-w-md space-y-6">
                <h5 className="text-2xl font-roboto text-left text-black mb-4 tracking-tight">
                    Register an Account
                </h5>

                <div className="flex items-center bg-white rounded-2xl shadow-lg px-4 py-3 space-x-3 transition hover:shadow-xl">
                    <Mail className="text-yellow-400" />
                    <input
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email Address"
                        className="flex-grow bg-transparent outline-none text-gray-700 placeholder:text-gray-400"
                    />
                </div>

                <div className="flex items-center bg-white rounded-2xl shadow-lg px-4 py-3 space-x-3 transition hover:shadow-xl">
                    <Mail className="text-yellow-400" />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        className="flex-grow bg-transparent outline-none text-gray-700 placeholder:text-gray-400"
                    />
                </div>

                <div className="flex items-center bg-white rounded-2xl shadow-lg px-4 py-3 space-x-3 transition hover:shadow-xl">
                    <Mail className="text-yellow-400" />
                    <input
                        type="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm Password"
                        className="flex-grow bg-transparent outline-none text-gray-700 placeholder:text-gray-400"
                    />
                </div>

                <button
                    onClick={() => console.log("Register")}
                    className="w-full bg-yellow-500 text-white font-semibold py-3 rounded-2xl shadow-md hover:bg-yellow-700 transition-all duration-200">
                    Register
                </button>

            </div>
        </div>
    );
};
