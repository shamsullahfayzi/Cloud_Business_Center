"use client";

import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Typography, 
  Paper, 
  Avatar, 
  Divider 
} from '@mui/material';
import { 
  LockOutlined, 
  PersonOutline, 
  StorefrontOutlined 
} from '@mui/icons-material';
import login, { Login_type } from '../api/auth';

// Tailwind CSS will be used for additional styling
const AdvancedLoginForm: React.FC = () => {
  const [role, setRole] = useState<'customer' | 'salesman' | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRoleSelect = (selectedRole: 'customer' | 'salesman') => {
    setRole(selectedRole);
  };
  const roleMapping: Record<'customer' | 'salesman', number> = {
    customer: 3,
    salesman: 2,
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Implement login logic here
    const credentials:Login_type = {
        email:email,
        password:password,
        role:roleMapping[role!]
    }
   const result = await login(credentials)
   console.log(result)
    console.log('Login', { role, email, password });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-purple-500 p-4">
      <Paper 
        elevation={12} 
        className="w-full max-w-md rounded-2xl overflow-hidden shadow-2xl transform transition-all  "
      >
        {/* Role Selection Section */}
        {!role ? (
          <div className="p-8 text-center">
            <Typography 
              variant="h4" 
              className="mb-6 font-bold text-gray-800"
            >
              Login as:
            </Typography>
            
            <div className="flex justify-center space-x-6">
              {/* Customer Role Button */}
              <button 
                onClick={() => handleRoleSelect('customer')}
                className="flex flex-col items-center p-4 border-2 border-transparent hover:border-blue-500 rounded-xl transition-all duration-300 group"
              >
                <Avatar 
                  className="w-24 h-24 mb-4 bg-blue-100 group-hover:bg-blue-200 transition-colors"
                >
                  <PersonOutline className="text-blue-600 w-12 h-12" />
                </Avatar>
                <Typography variant="h6" className="text-gray-700 group-hover:text-blue-600">
                  Customer
                </Typography>
              </button>

              {/* Salesman Role Button */}
              <button 
                onClick={() => handleRoleSelect('salesman')}
                className="flex flex-col items-center p-4 border-2 border-transparent hover:border-green-500 rounded-xl transition-all duration-300 group"
              >
                <Avatar 
                  className="w-24 h-24 mb-4 bg-green-100 group-hover:bg-green-200 transition-colors"
                >
                  <StorefrontOutlined className="text-green-600 w-12 h-12" />
                </Avatar>
                <Typography variant="h6" className="text-gray-700 group-hover:text-green-600">
                  Salesman
                </Typography>
              </button>
            </div>
          </div>
        ) : (
          // Login Form Section
          <form onSubmit={handleSubmit} className="p-8 space-y-6">
            <div className="flex items-center justify-between mb-4">
              <Typography 
                variant="h4" 
                className="font-bold text-gray-800 flex items-center"
              >
                <LockOutlined className="mr-2" />
                {role === 'customer' ? 'Customer' : 'Salesman'} Login
              </Typography>
              <button 
                type="button"
                onClick={() => setRole(null)}
                className="text-blue-600 hover:underline"
              >
                Change Role
              </button>
            </div>

            <TextField
              fullWidth
              label="Email"
              variant="outlined"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mb-4"
              required
            />

            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <div className="flex items-center justify-between mt-4">
              <a 
                href="#" 
                className="text-blue-600 hover:underline"
              >
                Forgot Password?
              </a>
            </div>

            <Button
              type="submit"
              variant="contained"
              fullWidth
              className="mt-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transition-all duration-300"
            >
              Sign In
            </Button>

            <Divider className="my-6">
              <Typography variant="body2" className="text-gray-500">
                New User?
              </Typography>
            </Divider>

            <Button
              variant="outlined"
              fullWidth
              className="border-blue-500 text-blue-500 hover:bg-blue-50"
            >
              Create an Account
            </Button>
          </form>
        )}
      </Paper>
    </div>
  );
};

export default AdvancedLoginForm;