import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, Sparkles } from 'lucide-react';
import { useAuth } from '../utils/AuthContext';
import AnimatedBackground from '../components/AnimatedBackground';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const success = await login(username, password);
    setLoading(false);
    if (success) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden chemical-container">
      <AnimatedBackground />
      
      {/* Floating chemical elements */}
      <div className="absolute inset-0 pointer-events-none">
        {['⚗️', '🧪', '⚛️', '🔬', '🧬'].map((emoji, index) => (
          <motion.div
            key={index}
            className="absolute text-4xl opacity-20"
            style={{
              left: `${20 + index * 15}%`,
              top: `${10 + index * 12}%`,
            }}
            animate={{
              y: [0, -30, 0],
              rotate: [0, 180, 360],
              scale: [1, 1.2, 1],
            }}
            transition={{
              duration: 6 + index,
              repeat: Infinity,
              ease: "easeInOut",
              delay: index * 0.8
            }}
          >
            {emoji}
          </motion.div>
        ))}
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 50, rotateX: -15 }}
        animate={{ opacity: 1, y: 0, rotateX: 0 }}
        transition={{ duration: 0.8, type: 'spring', stiffness: 100 }}
        className="w-full max-w-md relative z-10"
        style={{ transformStyle: 'preserve-3d' }}
      >
        <div className="glass-morphism rounded-3xl p-8 border-2 border-white/10 shadow-2xl relative overflow-hidden hover-lift">
          {/* Animated gradient overlay */}
          <div className="absolute inset-0 animated-gradient opacity-10 rounded-3xl" />
          
          {/* Chemical structure background */}
          <div className="absolute inset-0 opacity-5">
            <svg className="w-full h-full" viewBox="0 0 400 500">
              <circle cx="100" cy="100" r="20" fill="currentColor" />
              <circle cx="200" cy="150" r="15" fill="currentColor" />
              <circle cx="300" cy="200" r="18" fill="currentColor" />
              <line x1="100" y1="100" x2="200" y2="150" stroke="currentColor" strokeWidth="2" />
              <line x1="200" y1="150" x2="300" y2="200" stroke="currentColor" strokeWidth="2" />
            </svg>
          </div>
          
          <div className="relative z-10">
            <motion.div
              initial={{ scale: 0, rotateY: -180 }}
              animate={{ scale: 1, rotateY: 0 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-blue-500 via-purple-600 to-pink-500 flex items-center justify-center glow-effect mb-6 molecule-3d"
              whileHover={{ scale: 1.1, rotateY: 180 }}
            >
              <Sparkles className="w-10 h-10 text-white" />
            </motion.div>

            <motion.h2 
              className="text-4xl font-display font-bold text-center mb-2 text-gradient chemical-formula"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              ChemViz Portal
            </motion.h2>
            <motion.p 
              className="text-center text-blue-300/60 mb-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              Access your chemical equipment analytics
            </motion.p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
              >
                <label className="block text-sm font-medium mb-2 text-blue-200 chemical-formula">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="login-input w-full px-4 py-3 rounded-xl glass-morphism border border-white/20 text-gray-900 placeholder-gray-400 focus:text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all interactive-element"
                  placeholder="Enter your username"
                  required
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
              >
                <label className="block text-sm font-medium mb-2 text-blue-200 chemical-formula">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="login-input w-full px-4 py-3 rounded-xl glass-morphism border border-white/20 text-gray-900 placeholder-gray-400 focus:text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all interactive-element"
                  placeholder="Enter your password"
                  required
                />
              </motion.div>

              <motion.button
                whileHover={{ scale: 1.02, rotateY: 2 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={loading}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
                className="w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 hover:from-blue-500 hover:via-purple-500 hover:to-blue-500 font-semibold text-lg shadow-lg glow-effect button-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2 pulse-glow"
                style={{ transformStyle: 'preserve-3d' }}
              >
                <motion.div
                  animate={loading ? { rotate: 360 } : { rotate: 0 }}
                  transition={{ duration: 1, repeat: loading ? Infinity : 0, ease: "linear" }}
                >
                  <LogIn className="w-5 h-5" />
                </motion.div>
                <span>{loading ? 'Authenticating...' : 'Access Portal'}</span>
              </motion.button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-blue-300/60">
                Don't have an account?{' '}
                <Link
                  to="/register"
                  className="text-blue-400 hover:text-blue-300 font-semibold transition-colors"
                >
                  Sign up
                </Link>
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;