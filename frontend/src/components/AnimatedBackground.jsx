import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

const AnimatedBackground = () => {
  const canvasRef = useRef(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Chemical industry elements
    const molecules = [];
    const pipes = [];
    const particles = [];
    const bubbles = [];

    // Create molecular structures
    class Molecule {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 8 + 4;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.connections = [];
        this.color = `hsl(${200 + Math.random() * 60}, 70%, 60%)`;
        this.pulsePhase = Math.random() * Math.PI * 2;
      }

      update(mouseX, mouseY) {
        // Mouse interaction
        const dx = mouseX - this.x;
        const dy = mouseY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 150) {
          const force = (150 - distance) / 150;
          this.vx += (dx / distance) * force * 0.01;
          this.vy += (dy / distance) * force * 0.01;
        }

        this.x += this.vx;
        this.y += this.vy;
        this.pulsePhase += 0.02;

        // Boundary collision
        if (this.x < 0 || this.x > canvas.width) this.vx *= -0.8;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -0.8;
        
        // Keep in bounds
        this.x = Math.max(0, Math.min(canvas.width, this.x));
        this.y = Math.max(0, Math.min(canvas.height, this.y));
        
        // Friction
        this.vx *= 0.99;
        this.vy *= 0.99;
      }

      draw() {
        const pulse = Math.sin(this.pulsePhase) * 0.3 + 1;
        const size = this.size * pulse;
        
        // Outer glow
        ctx.beginPath();
        ctx.arc(this.x, this.y, size * 2, 0, Math.PI * 2);
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, size * 2);
        gradient.addColorStop(0, this.color.replace('60%', '20%'));
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;
        ctx.fill();
        
        // Main molecule
        ctx.beginPath();
        ctx.arc(this.x, this.y, size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        
        // Inner highlight
        ctx.beginPath();
        ctx.arc(this.x - size * 0.3, this.y - size * 0.3, size * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fill();
      }
    }

    // Create pipe network
    class Pipe {
      constructor() {
        this.startX = Math.random() * canvas.width;
        this.startY = Math.random() * canvas.height;
        this.endX = Math.random() * canvas.width;
        this.endY = Math.random() * canvas.height;
        this.width = Math.random() * 4 + 2;
        this.flow = 0;
        this.flowSpeed = Math.random() * 0.02 + 0.01;
      }

      update() {
        this.flow += this.flowSpeed;
        if (this.flow > 1) this.flow = 0;
      }

      draw() {
        // Pipe body
        ctx.beginPath();
        ctx.moveTo(this.startX, this.startY);
        ctx.lineTo(this.endX, this.endY);
        ctx.strokeStyle = 'rgba(100, 150, 200, 0.3)';
        ctx.lineWidth = this.width;
        ctx.stroke();
        
        // Flow animation
        const flowX = this.startX + (this.endX - this.startX) * this.flow;
        const flowY = this.startY + (this.endY - this.startY) * this.flow;
        
        ctx.beginPath();
        ctx.arc(flowX, flowY, this.width * 0.8, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 200, 255, 0.6)';
        ctx.fill();
      }
    }

    // Floating particles
    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = (Math.random() - 0.5) * 0.3;
        this.opacity = Math.random() * 0.5 + 0.2;
        this.color = `hsl(${180 + Math.random() * 80}, 60%, 70%)`;
      }

      update(mouseX, mouseY) {
        // Mouse repulsion
        const dx = mouseX - this.x;
        const dy = mouseY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 100) {
          const force = (100 - distance) / 100;
          this.vx -= (dx / distance) * force * 0.005;
          this.vy -= (dy / distance) * force * 0.005;
        }

        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color.replace('70%', `${this.opacity * 70}%`);
        ctx.fill();
      }
    }

    // Bubble effects
    class Bubble {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + 50;
        this.size = Math.random() * 20 + 10;
        this.vy = -(Math.random() * 2 + 1);
        this.vx = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.3 + 0.1;
        this.wobble = Math.random() * Math.PI * 2;
      }

      update() {
        this.y += this.vy;
        this.x += this.vx + Math.sin(this.wobble) * 0.5;
        this.wobble += 0.02;
        
        if (this.y < -50) {
          this.y = canvas.height + 50;
          this.x = Math.random() * canvas.width;
        }
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size);
        gradient.addColorStop(0, `rgba(100, 200, 255, ${this.opacity})`);
        gradient.addColorStop(0.7, `rgba(150, 220, 255, ${this.opacity * 0.5})`);
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;
        ctx.fill();
        
        // Bubble highlight
        ctx.beginPath();
        ctx.arc(this.x - this.size * 0.3, this.y - this.size * 0.3, this.size * 0.2, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity * 0.8})`;
        ctx.fill();
      }
    }

    // Initialize elements
    for (let i = 0; i < 25; i++) {
      molecules.push(new Molecule());
    }
    
    for (let i = 0; i < 8; i++) {
      pipes.push(new Pipe());
    }
    
    for (let i = 0; i < 50; i++) {
      particles.push(new Particle());
    }
    
    for (let i = 0; i < 15; i++) {
      bubbles.push(new Bubble());
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw pipes first (background)
      pipes.forEach(pipe => {
        pipe.update();
        pipe.draw();
      });

      // Draw molecular connections
      molecules.forEach((mol1, i) => {
        molecules.slice(i + 1).forEach(mol2 => {
          const dx = mol1.x - mol2.x;
          const dy = mol1.y - mol2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 120) {
            ctx.beginPath();
            ctx.moveTo(mol1.x, mol1.y);
            ctx.lineTo(mol2.x, mol2.y);
            const opacity = (120 - distance) / 120;
            ctx.strokeStyle = `rgba(100, 180, 255, ${opacity * 0.3})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        });
      });

      // Update and draw all elements
      molecules.forEach(molecule => {
        molecule.update(mousePosition.x, mousePosition.y);
        molecule.draw();
      });

      particles.forEach(particle => {
        particle.update(mousePosition.x, mousePosition.y);
        particle.draw();
      });

      bubbles.forEach(bubble => {
        bubble.update();
        bubble.draw();
      });

      requestAnimationFrame(animate);
    }

    animate();
    setIsLoaded(true);

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <>
      {/* 3D Chemical Industry Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {/* Animated gradient background */}
        <div 
          className="absolute inset-0 opacity-40"
          style={{
            background: `
              radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, 
                rgba(59, 130, 246, 0.3) 0%, 
                rgba(139, 92, 246, 0.2) 25%, 
                rgba(236, 72, 153, 0.1) 50%, 
                transparent 70%
              ),
              linear-gradient(135deg, 
                rgba(15, 23, 42, 0.9) 0%, 
                rgba(30, 58, 138, 0.8) 25%, 
                rgba(59, 130, 246, 0.6) 50%, 
                rgba(139, 92, 246, 0.4) 75%, 
                rgba(15, 23, 42, 0.9) 100%
              )
            `,
            transform: `translate(${mousePosition.x * 0.02}px, ${mousePosition.y * 0.02}px)`,
            transition: 'transform 0.1s ease-out'
          }}
        />
        
        {/* Chemical equipment silhouettes */}
        <div 
          className="absolute inset-0 opacity-20"
          style={{
            transform: `translate(${mousePosition.x * 0.01}px, ${mousePosition.y * 0.01}px)`,
            transition: 'transform 0.2s ease-out'
          }}
        >
          {/* Factory pipes */}
          <svg className="absolute top-0 left-0 w-full h-full" viewBox="0 0 1920 1080">
            <defs>
              <linearGradient id="pipeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="rgba(59, 130, 246, 0.3)" />
                <stop offset="50%" stopColor="rgba(139, 92, 246, 0.2)" />
                <stop offset="100%" stopColor="rgba(236, 72, 153, 0.1)" />
              </linearGradient>
            </defs>
            
            {/* Horizontal pipes */}
            <rect x="0" y="200" width="1920" height="20" fill="url(#pipeGradient)" rx="10" />
            <rect x="0" y="400" width="1920" height="15" fill="url(#pipeGradient)" rx="7" />
            <rect x="0" y="600" width="1920" height="25" fill="url(#pipeGradient)" rx="12" />
            <rect x="0" y="800" width="1920" height="18" fill="url(#pipeGradient)" rx="9" />
            
            {/* Vertical pipes */}
            <rect x="300" y="0" width="20" height="1080" fill="url(#pipeGradient)" rx="10" />
            <rect x="600" y="0" width="15" height="1080" fill="url(#pipeGradient)" rx="7" />
            <rect x="900" y="0" width="25" height="1080" fill="url(#pipeGradient)" rx="12" />
            <rect x="1200" y="0" width="18" height="1080" fill="url(#pipeGradient)" rx="9" />
            <rect x="1500" y="0" width="22" height="1080" fill="url(#pipeGradient)" rx="11" />
            
            {/* Chemical tanks */}
            <circle cx="200" cy="300" r="80" fill="rgba(59, 130, 246, 0.1)" stroke="rgba(59, 130, 246, 0.3)" strokeWidth="2" />
            <circle cx="1700" cy="500" r="100" fill="rgba(139, 92, 246, 0.1)" stroke="rgba(139, 92, 246, 0.3)" strokeWidth="2" />
            <circle cx="800" cy="800" r="60" fill="rgba(236, 72, 153, 0.1)" stroke="rgba(236, 72, 153, 0.3)" strokeWidth="2" />
            
            {/* Reactor vessels */}
            <rect x="1400" y="200" width="120" height="200" fill="rgba(59, 130, 246, 0.1)" stroke="rgba(59, 130, 246, 0.3)" strokeWidth="2" rx="20" />
            <rect x="100" y="600" width="100" height="180" fill="rgba(139, 92, 246, 0.1)" stroke="rgba(139, 92, 246, 0.3)" strokeWidth="2" rx="15" />
          </svg>
        </div>
        
        {/* Animated canvas overlay */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 pointer-events-none"
          style={{ opacity: isLoaded ? 0.8 : 0 }}
        />
        
        {/* Floating chemical formulas */}
        <div 
          className="absolute inset-0 overflow-hidden"
          style={{
            transform: `translate(${mousePosition.x * -0.005}px, ${mousePosition.y * -0.005}px)`,
            transition: 'transform 0.3s ease-out'
          }}
        >
          {['H₂SO₄', 'NaOH', 'C₆H₁₂O₆', 'NH₃', 'CO₂', 'H₂O', 'CH₄', 'C₂H₅OH'].map((formula, index) => (
            <motion.div
              key={formula}
              className="absolute text-blue-300/30 font-mono text-lg"
              style={{
                left: `${(index * 23 + 10) % 90}%`,
                top: `${(index * 17 + 15) % 80}%`,
              }}
              animate={{
                y: [0, -20, 0],
                opacity: [0.3, 0.6, 0.3],
              }}
              transition={{
                duration: 4 + index,
                repeat: Infinity,
                ease: "easeInOut",
                delay: index * 0.5
              }}
            >
              {formula}
            </motion.div>
          ))}
        </div>
        
        {/* Grid pattern overlay */}
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `
              linear-gradient(rgba(59, 130, 246, 0.3) 1px, transparent 1px),
              linear-gradient(90deg, rgba(59, 130, 246, 0.3) 1px, transparent 1px)
            `,
            backgroundSize: '50px 50px',
            transform: `translate(${mousePosition.x * 0.005}px, ${mousePosition.y * 0.005}px)`,
            transition: 'transform 0.1s ease-out'
          }}
        />
      </div>
    </>
  );
};

export default AnimatedBackground;