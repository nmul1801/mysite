import { useState, useEffect } from 'react';

export const useResponsiveChart = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    // Check initial size
    checkScreenSize();

    // Add event listener
    window.addEventListener('resize', checkScreenSize);

    // Cleanup
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  return {
    isMobile,
    fontSize: isMobile ? 10 : 12,
    angle: isMobile ? -60 : -45,
    height: isMobile ? 100 : 80
  };
}; 