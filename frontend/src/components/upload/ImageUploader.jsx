// Role : Selection d'une image (drag & drop ou clic) + apercu local avant envoi.

import { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";

export default function ImageUploader({ onFileSelected }) {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  function selectFile(file) {
    if (!file) {
      return;
    }
    setPreviewUrl(URL.createObjectURL(file));
    onFileSelected(file);
  }

  function handleChange(event) {
    selectFile(event.target.files?.[0]);
  }

  function handleDrop(event) {
    event.preventDefault();
    setDragActive(false);
    selectFile(event.dataTransfer.files?.[0]);
  }

  function handleDragOver(event) {
    event.preventDefault();
    setDragActive(true);
  }

  function handleDragLeave() {
    setDragActive(false);
  }

  return (
    <div>
      <div
        className={`upload-dropzone${dragActive ? " drag-active" : ""}`}
        onClick={() => inputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        role="button"
        tabIndex={0}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            inputRef.current?.click();
          }
        }}
      >
        <span className="upload-icon">
          <UploadCloud size={26} />
        </span>
        <p className="upload-title">Drag &amp; drop your image, or click to browse</p>
        <p className="upload-hint">JPG, JPEG or PNG — up to 10 MB</p>
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png,image/jpeg,image/png"
          onChange={handleChange}
          style={{ display: "none" }}
        />
      </div>

      {previewUrl && <img src={previewUrl} alt="Selected preview" className="upload-preview" />}
    </div>
  );
}
