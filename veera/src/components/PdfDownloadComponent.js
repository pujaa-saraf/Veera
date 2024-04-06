import React from 'react'
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';


export default function PdfDownloadComponent() {

    const handleDownloadPDF = () => {
        const input = document.getElementById('search_result');
        html2canvas(input, {
          scale: 2,
          width: input.scrollWidth,
          windowWidth: input.scrollWidth
        }).then((canvas) => {
          const imgWidth = 210;
          const pageHeight = 295;
          const imgHeight = canvas.height * imgWidth / canvas.width;
          let heightLeft = imgHeight;
          const pdf = new jsPDF('p', 'mm', 'a4');
          let position = 0;
    
          pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
    
          while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
          }
          pdf.save('downloaded-file.pdf');
        });
      };
    
      return (
        <div className='flex justify-center mt-16 mb-16'><button className='p-4 bg-blue-500 rounded-lg text-white text-lg font-semibold' onClick={handleDownloadPDF}>Download as PDF</button></div>
      );
}
